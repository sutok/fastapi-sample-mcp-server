from datetime import datetime, time, timedelta
from typing import Optional
from fastapi import HTTPException
from .config import settings


def validate_business_hours(reservation_time: time) -> bool:
    """営業時間内かどうかを確認"""
    start = settings.get_business_hours_start()
    end = settings.get_business_hours_end()
    return start <= reservation_time <= end


def validate_reservation_date(date: datetime) -> bool:
    """予約可能な日付かどうかを確認"""
    today = datetime.now().date()
    max_date = today + timedelta(days=settings.RESERVATION_ADVANCE_DAYS)
    return today <= date.date() <= max_date


def validate_cancellation_time(reservation_time: datetime) -> bool:
    """キャンセル可能な時間かどうかを確認"""
    now = datetime.now()
    cancellation_limit = reservation_time - timedelta(
        hours=settings.CANCELLATION_HOURS_BEFORE
    )
    return now <= cancellation_limit


def validate_reservation_duration(duration_minutes: int) -> bool:
    """予約時間の長さが有効かどうかを確認"""
    min_duration = settings.MIN_RESERVATION_MINUTES
    max_duration = settings.MAX_RESERVATION_HOURS * 60
    return (
        min_duration <= duration_minutes <= max_duration
        and duration_minutes % settings.TIME_SLOT_MINUTES == 0
    )


def calculate_cancellation_fee(reservation_time: datetime) -> int:
    """キャンセル料金を計算"""
    now = datetime.now()
    hours_before = (reservation_time - now).total_seconds() / 3600

    if hours_before >= settings.FREE_CANCELLATION_HOURS:
        return 0
    elif reservation_time.date() == now.date():
        return settings.SAME_DAY_CANCELLATION_FEE
    else:
        return 50  # 24時間以内のキャンセルは50%


def format_reservation_number(number: int) -> str:
    """予約番号をフォーマット"""
    prefix = settings.RESERVATION_NUMBER_PREFIX or ""
    formatted_number = settings.RESERVATION_NUMBER_FORMAT % number
    return f"{prefix}{formatted_number}"
