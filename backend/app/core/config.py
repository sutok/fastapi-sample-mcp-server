from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv
import json
import warnings
from datetime import time

load_dotenv()


class Settings(BaseSettings):
    # モデルの設定
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,  # 環境変数の大文字小文字を区別
        extra="ignore",  # 未定義の環境変数を無視
    )

    # 環境変数との対応をより明確に
    APP_NAME: str = Field(default="Sample FastAPI")
    ENVIRONMENT: str = Field(
        default="development",
        env="ENVIRONMENT",  # 環境変数名を明示的に指定
    )
    DEBUG: bool = False
    API_V1_STR: str = Field(default="/api/v1")

    # セキュリティ設定
    SECRET_KEY: str = Field(...)  # descriptionを削除
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS設定
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
    )

    # 開発環境の場合、エミュレータのホストを設定
    if ENVIRONMENT == "development":
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"
        os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        """
        CORS設定の検証と変換を行う

        Args:
            v: 文字列またはリストの形式のオリジン設定

        Returns:
            検証済みのオリジンリスト
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Firebase設定
    FIREBASE_CREDENTIALS_PATH: str = os.path.join(
        os.getcwd(), "firebase/credentials/service-account.json"
    )

    @property
    def firebase_credentials(self) -> dict:
        """
        Firebaseの認証情報を取得する

        Returns:
            dict: サービスアカウントの認証情報
        """
        with open(self.FIREBASE_CREDENTIALS_PATH, "r") as f:
            return json.load(f)

    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # 予約制限
    MAX_CONCURRENT_RESERVATIONS: int = 5
    RESERVATION_ADVANCE_DAYS: int = 1
    CANCELLATION_HOURS_BEFORE: int = 24

    # 営業時間設定
    BUSINESS_HOURS_START: str = "10:00"
    BUSINESS_HOURS_END: str = "22:00"
    TIME_SLOT_MINUTES: int = 30
    MAX_RESERVATION_HOURS: int = 3
    MIN_RESERVATION_MINUTES: int = 30

    # キャンセルポリシー
    FREE_CANCELLATION_HOURS: int = 24
    SAME_DAY_CANCELLATION_FEE: int = 100

    # 順番表示設定
    RESERVATION_NUMBER_FORMAT: str = "%04d"
    RESERVATION_NUMBER_PREFIX: Optional[str] = None

    # 待ち時間計算
    WAIT_TIME_UPDATE_INTERVAL: int = 5
    DEFAULT_APPOINTMENT_DURATION: int = 30

    # 表示制限
    MAX_NEXT_APPOINTMENTS_DISPLAY: int = 5
    LONG_WAIT_TIME_THRESHOLD: int = 60

    # レート制限
    RATE_LIMIT_RESERVATION_CREATE: int = 10
    RATE_LIMIT_RESERVATION_UPDATE: int = 20
    RATE_LIMIT_AVAILABILITY_CHECK: int = 60
    RATE_LIMIT_OTHER_ENDPOINTS: int = 30

    def get_business_hours_start(self) -> time:
        """営業開始時間をtime型で取得"""
        hours, minutes = map(int, self.BUSINESS_HOURS_START.split(":"))
        return time(hour=hours, minute=minutes)

    def get_business_hours_end(self) -> time:
        """営業終了時間をtime型で取得"""
        hours, minutes = map(int, self.BUSINESS_HOURS_END.split(":"))
        return time(hour=hours, minute=minutes)


# グローバル設定インスタンスの作成
settings = Settings()


# デバッグモードに応じて警告の表示を制御
def configure_warnings():
    if not settings.DEBUG:
        # 特定の警告を無視
        warnings.filterwarnings(
            "ignore",
            message="Detected filter using positional arguments.*",
            category=UserWarning,
            module="google.cloud.firestore_v1.base_collection",
        )
