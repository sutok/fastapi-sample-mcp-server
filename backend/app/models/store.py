from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class StoreStatus(str, Enum):
    """店舗ステータス"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"


class StoreBase(BaseModel):
    """店舗の基本情報モデル"""

    company_id: str = Field(..., description="所属企業ID")
    name: str = Field(..., description="店舗名")
    address: str = Field(..., description="住所")
    phone: str = Field(..., description="電話番号")
    email: Optional[str] = Field(None, description="メールアドレス")
    business_hours: str = Field(..., description="営業時間")
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v == "":
            raise ValueError("店舗名は必須です")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        if v == "":
            raise ValueError("住所は必須です")
        return v


class StoreCreate(StoreBase):
    """店舗作成モデル"""

    pass


class StoreUpdate(BaseModel):
    """店舗更新モデル"""

    name: Optional[str] = Field(None, description="店舗名")
    address: Optional[str] = Field(None, description="住所")
    phone: Optional[str] = Field(None, description="電話番号")
    email: Optional[str] = Field(None, description="メールアドレス")
    business_hours: Optional[str] = Field(None, description="営業時間")
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )
    status: Optional[StoreStatus] = Field(None, description="ステータス")


class StoreInDBBase(StoreBase):
    """データベース保存用の基本フィールド"""

    id: str
    status: StoreStatus = StoreStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StoreInDB(StoreInDBBase):
    """データベース内の店舗モデル（内部処理用）"""

    pass


class Store(StoreInDBBase):
    """APIレスポンス用店舗モデル"""

    class Config:
        from_attributes = True
