from typing import List, Optional
from datetime import datetime, date, timedelta, time
from firebase_admin import firestore
from ..models.reservation import ReservationCreate, ReservationUpdate, ReservationStatus
from ..core.firebase import get_firestore
from ..core.config import settings
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

    async def _generate_reception_number(self, reservation_at: datetime) -> int:
        """
        指定された日付の受付番号を生成

        Args:
            reservation_date (date): 予約日

        Returns:
            int: 生成された受付番号
        """
        # 指定日の開始時刻と終了時刻を設定
        start_of_day = reservation_at.strftime("%Y-%m-%d 00:00:00")
        end_of_day = (reservation_at + timedelta(days=1)).strftime("%Y-%m-%d 23:59:59")

        # 指定日の予約を全て取得
        query = (
            self.collection.where("reservation_at", ">=", start_of_day)
            .where("reservation_at", "<", end_of_day)
            .order_by("reservation_at")
            .order_by("reception_number", direction=firestore.Query.DESCENDING)
            .limit(1)
        )

        docs = query.get()

        # その日の最後の受付番号を取得し、+1した値を返す
        if docs:
            return len(docs) + 1

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

        # 受付番号を生成。順番のみなので時刻は現在時刻
        reception_number = await self._generate_reception_number(current_time)

        reservation_data = {
            "user_id": user_id,
            "company_id": reservation.company_id,
            "branch_id": reservation.branch_id,
            "reservation_at": reservation.reservation_at,
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
            # 予約日時の年月日で予約数をカウント
            start_of_day = reservation_data["reservation_at"].replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_of_day = start_of_day + timedelta(days=1)

            existing_query = (
                self.collection.where("reservation_at", ">=", start_of_day)
                .where("reservation_at", "<", end_of_day)
                .get()
            )
            # 受付番号初期化
            new_number = 0
            if len(existing_query) > 0:
                # 重複が見つかった場合は、再度受付番号を生成
                new_number = len(existing_query) + 1
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
                "reservation_at": reservation.reservation_at,
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
        user_id: Optional[str] = None,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        target_date: Optional[date] = None,
        status: Optional[str] = None,
    ) -> List[dict]:
        """
        ユーザーの予約一覧を取得

        Args:
            user_id (str): ユーザーID
            skip (int): スキップする件数
            limit (int): 取得する件数
            target_date (date, optional): 検索日
            status (str, optional): 予約ステータス

        Returns:
            List[dict]: 予約一覧
        """
        query = self.collection

        if user_id:
            query = query.where("user_id", "==", user_id)

        if company_id:
            query = query.where("company_id", "==", company_id)

        if branch_id:
            query = query.where("branch_id", "==", branch_id)

        if target_date:
            from_datetime = datetime.combine(target_date, time.min)
            to_datetime = datetime.combine(target_date, time.max)
            query = query.where("reservation_at", ">=", from_datetime)
            query = query.where("reservation_at", "<=", to_datetime)

        if status:
            query = query.where("status", "==", status)

        # 日付でソート
        query = query.order_by("reservation_at", direction=firestore.Query.DESCENDING)

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
        date_timestamp = reservation_date.strftime("%Y-%m-%d")
        next_day = (reservation_date + timedelta(days=1)).strftime("%Y-%m-%d")

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
        date_timestamp = reservation_date.strftime("%Y-%m-%d")
        next_day = (reservation_date + timedelta(days=1)).strftime("%Y-%m-%d")

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
            update_data["reservation_date"] = update_data["reservation_date"].strftime(
                "%Y-%m-%d"
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

    async def get_available_slots(self, date_input):
        if isinstance(date_input, str):
            date_obj = datetime.strptime(date_input, "%Y-%m-%d").date()
        elif isinstance(date_input, date):
            date_obj = date_input
        else:
            raise ValueError("date_input must be str or datetime.date")

        # 企業コード・店舗コード（必要なら利用）
        company_id = None
        branch_id = None

        # 営業時間・枠生成
        business_start = settings.get_business_hours_start()
        business_end = settings.get_business_hours_end()
        slot_minutes = settings.TIME_SLOT_MINUTES

        slots = []
        current = datetime.combine(date_obj, business_start)
        end = datetime.combine(date_obj, business_end)
        while current < end:
            slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=slot_minutes)

        # Firestoreから予約済み枠を取得
        date_str = date_obj.strftime("%Y-%m-%d")
        query = self.collection.where("reservation_date", "==", date_str)
        if company_id is not None:
            query = query.where("company_id", "==", company_id)
        if branch_id is not None:
            query = query.where("branch_id", "==", branch_id)

        reservations = query.get()
        # 時間ごとにuser_idをマッピング
        reserved_map = {
            doc.to_dict().get("reservation_time"): doc.to_dict().get("user_id")
            for doc in reservations
        }

        # available_slotsリストを作成
        available_slots = [
            {
                "time": slot,
                "is_reserved": slot in reserved_map,
                "user_id": reserved_map.get(slot) if slot in reserved_map else None,
            }
            for slot in slots
        ]

        return available_slots

    async def get_daily_summary(
        self, company_id: str, branch_id: str, date: date
    ) -> dict:
        """
        指定日の予約状況サマリーを取得

        Args:
            company_id (str): 企業ID
            branch_id (str): 店舗ID
            date (date): 対象日

        Returns:
            dict: 予約状況サマリー
        """
        # 当日の予約を取得
        query = (
            self.collection.where("company_id", "==", company_id)
            .where("branch_id", "==", branch_id)
            .where("reservation_at", ">=", datetime.combine(date, time.min))
            .where("reservation_at", "<=", datetime.combine(date, time.max))
        )

        docs = query.stream()

        # 待機中の予約をカウント
        waiting_count = 0
        latest_reception_number = 0
        current_number = None

        for doc in docs:
            data = doc.to_dict()
            if data.get("status") == "accepted":
                waiting_count += 1
                reception_number = data.get("reception_number", 0)
                latest_reception_number = max(latest_reception_number, reception_number)

                # 現在の呼び出し番号を取得（statusがconfirmedの最新の予約）
                if data.get("status") == "confirmed":
                    current_number = reception_number

        return {
            "current_time": datetime.now(),
            "business_hours": {
                "morning_start": "10:00",
                "morning_end": "13:00",
                "afternoon_start": "14:00",
                "afternoon_end": "17:00",
            },
            "current_number": current_number,
            "latest_reception_number": latest_reception_number,
            "waiting_count": waiting_count,
        }


# CRUDReservationのインスタンスを作成
crud_reservation = CRUDReservation()
