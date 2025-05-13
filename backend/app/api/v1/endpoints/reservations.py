from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Any
from datetime import datetime, date
from ....crud.crud_reservation import crud_reservation
from ....models.reservation import (
    Reservation,
    ReservationCreate,
    ReservationUpdate,
    ReservationInDB,
    ReservationSummary,
)
from ....core.security import SecurityService
from ....crud.crud_company import crud_company
from ....crud.crud_branch import crud_branch

router = APIRouter()


@router.post("/", response_model=Reservation)
async def create_reservation(
    reservation: ReservationCreate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    新規予約を作成

    Args:
        reservation (ReservationCreate): 予約情報
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        Reservation: 作成された予約情報
    """
    return await crud_reservation.create(
        reservation=reservation, user_id=current_user["uid"]
    )


@router.get("/", response_model=List[Reservation])
async def read_reservations(
    current_user: Optional[dict] = Depends(SecurityService.verify_firebase_token),
    company_id: Optional[str] = Query(None),
    branch_id: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    target_date: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    ユーザーの予約一覧を取得

    Args:
        current_user (dict): 現在のユーザー情報（依存性注入）
        company_id: company_id
        branch_id: branch_id
        skip (int): スキップする件数
        limit (int): 取得する件数
        target_date (date, optional): 検索日
        status (str, optional): 予約ステータス

    Returns:
        List[Reservation]: 予約一覧
    """
    if target_date:
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    else:
        target_date = datetime.now().date()

    return await crud_reservation.get_multi_by_user(
        user_id=current_user["uid"],
        company_id=company_id,
        branch_id=branch_id,
        skip=skip,
        limit=limit,
        target_date=target_date,
        status=status,
    )


@router.get("/{reservation_id}", response_model=Reservation)
async def read_reservation(
    reservation_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    特定の予約情報を取得

    Args:
        reservation_id (str): 予約ID
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        Reservation: 予約情報
    """
    reservation = await crud_reservation.get(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")
    if reservation.user_id != current_user["uid"]:
        raise HTTPException(
            status_code=403, detail="この予約にアクセスする権限がありません"
        )
    return reservation


@router.put("/{reservation_id}", response_model=Reservation)
async def update_reservation(
    reservation_id: str,
    reservation_update: ReservationUpdate,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
    status: Optional[str] = None,
):
    """
    予約情報を更新

    Args:
        reservation_id (str): 予約ID
        reservation_update (ReservationUpdate): 更新する予約情報
        current_user (dict): 現在のユーザー情報（依存性注入）
        status (str, optional): 予約ステータス

    Returns:
        Reservation: 更新された予約情報
    """
    reservation = await crud_reservation.get(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")
    if reservation.user_id != current_user["uid"]:
        raise HTTPException(
            status_code=403, detail="この予約を更新する権限がありません"
        )
    if status:
        reservation_update.status = status

    return await crud_reservation.update(
        reservation_id=reservation_id, reservation_update=reservation_update
    )


@router.delete("/{reservation_id}")
async def delete_reservation(
    reservation_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    予約をキャンセル

    Args:
        reservation_id (str): 予約ID
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        dict: キャンセル完了メッセージ
    """
    reservation = await crud_reservation.get(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")
    if reservation.user_id != current_user["uid"]:
        raise HTTPException(
            status_code=403, detail="この予約をキャンセルする権限がありません"
        )

    await crud_reservation.delete(reservation_id)
    return {"message": "予約が正常にキャンセルされました"}


@router.get("/availability/{date}", response_model=List[dict])
async def check_availability(date: date):
    """
    指定日の予約可能な時間枠を取得

    Args:
        date (date): 確認したい日付

    Returns:
        List[dict]: 利用可能な時間枠のリスト
    """
    return await crud_reservation.get_available_slots(date)


@router.get("/{company_id}/{branch_id}/summary", response_model=ReservationSummary)
async def get_reservation_summary(
    company_id: str,
    branch_id: str,
    current_user: dict = Depends(SecurityService.verify_firebase_token),
):
    """
    指定企業・店舗の当日の予約状況サマリーを取得

    Args:
        company_id (str): 企業ID
        branch_id (str): 店舗ID
        current_user (dict): 現在のユーザー情報（依存性注入）

    Returns:
        ReservationSummary: 予約状況サマリー
    """
    # 企業と店舗の存在確認
    company = await crud_company.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="企業が見つかりません")

    branch = await crud_branch.get(branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="店舗が見つかりません")

    # 当日の予約状況サマリーを取得
    summary = await crud_reservation.get_daily_summary(
        company_id=company_id, branch_id=branch_id, date=datetime.now().date()
    )

    return ReservationSummary(**summary)
