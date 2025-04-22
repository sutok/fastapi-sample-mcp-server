from typing import List, Optional
from datetime import datetime, date, timedelta
from firebase_admin import firestore
from ..models.reservation import ReservationCreate, ReservationUpdate, ReservationStatus
from ..core.firebase import get_firestore
import logging

logger = logging.getLogger(__name__)


class CRUDReservation:
    def __init__(self):
        """
        予約CRUD操作用クラスの初期化
        Firestoreのクライアントを設定
        """
        self.db = get_firestore()
        self.collection = self.db.collection("reservations")

    def _date_to_timestamp(self, date_obj: date) -> datetime:
        """dateオブジェクトをdatetimeに変換"""
        return datetime.combine(date_obj, datetime.min.time())

    async def _generate_reception_number(self, reservation_date: date) -> int:
        """
        指定された日付の受付番号を生成

        Args:
            reservation_date (date): 予約日

        Returns:
            int: 生成された受付番号
        """
        # 指定日の開始時刻と終了時刻を設定
        start_of_day = self._date_to_timestamp(reservation_date)
        end_of_day = self._date_to_timestamp(reservation_date + timedelta(days=1))

        # 指定日の予約を全て取得
        query = (
            self.collection.where("reservation_date", ">=", start_of_day)
            .where("reservation_date", "<", end_of_day)
            .order_by("reservation_date")
            .order_by("reception_number", direction=firestore.Query.DESCENDING)
            .limit(1)
        )

        docs = query.get()

        # その日の最後の受付番号を取得し、+1した値を返す
        if docs:
            last_number = docs[0].to_dict().get("reception_number", 0)
            return last_number + 1

        # その日の最初の予約の場合は1を返す
        return 1

    async def create(self, reservation: ReservationCreate, user_id: str) -> dict:
        """
        新規予約を作成

        Args:
            reservation (ReservationCreate): 予約情報
            user_id (str): ユーザーID

        Returns:
            dict: 作成された予約情報
        """
        current_time = datetime.utcnow()

        # 受付番号を生成
        reception_number = await self._generate_reception_number(
            reservation.reservation_date
        )

        reservation_data = {
            "user_id": user_id,
            "reservation_date": self._date_to_timestamp(reservation.reservation_date),
            "reservation_time": reservation.reservation_time,
            "notes": reservation.notes,
            "status": ReservationStatus.CONFIRMED.value,
            "reception_number": reception_number,
            "created_at": current_time,
            "updated_at": current_time,
        }

        # トランザクションを使用して、受付番号の重複を防ぐ
        transaction = self.db.transaction()

        @firestore.transactional
        def create_in_transaction(transaction, reservation_data):
            # 受付番号の重複チェック
            existing_query = self.collection.where(
                "reservation_date", "==", reservation_data["reservation_date"]
            ).where("reception_number", "==", reception_number)

            if len(existing_query.get()) > 0:
                # 重複が見つかった場合は、再度受付番号を生成
                new_number = reception_number + 1
                reservation_data["reception_number"] = new_number

            # ドキュメントを作成
            doc_ref = self.collection.document()
            transaction.set(doc_ref, reservation_data)
            return doc_ref, reservation_data

        try:
            doc_ref, final_data = create_in_transaction(transaction, reservation_data)

            # 予約作成のログを出力
            logger.info(
                f"New reservation created: {doc_ref.id}, Reception number: {final_data['reception_number']}"
            )
            logger.debug(f"Reservation details: {final_data}")

            response_data = {
                **final_data,
                "id": doc_ref.id,
                "reservation_date": reservation.reservation_date,
            }
            return response_data

        except Exception as e:
            logger.error(f"Error creating reservation: {e}")
            raise

    async def get(self, reservation_id: str) -> Optional[dict]:
        """
        予約IDで予約情報を取得

        Args:
            reservation_id (str): 予約ID

        Returns:
            Optional[dict]: 予約情報
        """
        doc = self.collection.document(reservation_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            # datetimeからdateに変換して返す
            if "reservation_date" in data:
                data["reservation_date"] = data["reservation_date"].date()
            return data
        return None

    async def get_multi_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[dict]:
        """
        ユーザーの予約一覧を取得

        Args:
            user_id (str): ユーザーID
            skip (int): スキップする件数
            limit (int): 取得する件数
            date_from (date, optional): 検索開始日
            date_to (date, optional): 検索終了日

        Returns:
            List[dict]: 予約一覧
        """
        query = self.collection.where("user_id", "==", user_id)

        if date_from:
            query = query.where(
                "reservation_date", ">=", self._date_to_timestamp(date_from)
            )
        if date_to:
            query = query.where(
                "reservation_date",
                "<",
                self._date_to_timestamp(date_to + timedelta(days=1)),
            )

        # 日付でソート
        query = query.order_by("reservation_date")

        docs = query.limit(limit).offset(skip).get()
        reservations = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            # datetimeからdateに変換
            if "reservation_date" in data:
                data["reservation_date"] = data["reservation_date"].date()
            reservations.append(data)
        return reservations

    async def get_count_resavations(self, reservation_date: date) -> int:
        """
        指定された日付の予約数を取得

        Args:
            reservation_date (date): 日付

        Returns:
            int: 予約数
        """
        # dateをdatetimeに変換
        date_timestamp = self._date_to_timestamp(reservation_date)
        next_day = self._date_to_timestamp(reservation_date + timedelta(days=1))

        query = (
            self.collection.where("reservation_date", ">=", date_timestamp)
            .where("reservation_date", "<", next_day)
            .where("status", "==", ReservationStatus.CONFIRMED.value)
        )

        docs = query.get()
        return len(docs)

    async def is_time_slot_taken(
        self, reservation_date: date, reservation_time: str
    ) -> bool:
        """
        指定された時間枠が既に予約されているかチェック

        Args:
            reservation_date (date): 日付
            reservation_time (str): 時間枠

        Returns:
            bool: 予約済みの場合True
        """
        # dateをdatetimeに変換
        date_timestamp = self._date_to_timestamp(reservation_date)
        next_day = self._date_to_timestamp(reservation_date + timedelta(days=1))

        # whereメソッドを使用（filterではなく）
        query = (
            self.collection.where("reservation_date", ">=", date_timestamp)
            .where("reservation_date", "<", next_day)
            .where("reservation_time", "==", reservation_time)
            .where("status", "==", ReservationStatus.CONFIRMED.value)
        )

        docs = query.get()
        return len(docs) > 0

    async def update(
        self, reservation_id: str, reservation_update: ReservationUpdate
    ) -> Optional[dict]:
        """予約情報を更新"""
        update_data = reservation_update.dict(exclude_unset=True)
        if "reservation_date" in update_data:
            update_data["reservation_date"] = self._date_to_timestamp(
                update_data["reservation_date"]
            )
        update_data["updated_at"] = datetime.utcnow()

        doc_ref = self.collection.document(reservation_id)
        if doc_ref.get().exists:
            doc_ref.update(update_data)
            return await self.get(reservation_id)
        return None

    async def delete(self, reservation_id: str) -> bool:
        """予約を削除"""
        doc_ref = self.collection.document(reservation_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False


# CRUDReservationのインスタンスを作成
crud_reservation = CRUDReservation()
