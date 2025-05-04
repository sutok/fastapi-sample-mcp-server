from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """ユーザーの基本情報モデル"""

    email: EmailStr = Field(..., description="メールアドレス")
    username: str = Field(..., description="ユーザー名")
    is_active: bool = Field(default=True, description="アクティブ状態")
    role: str = Field(
        default="user",
        description="ユーザーのロール",
        enum=["system_admin", "company_admin", "store_admin", "staff", "user"],
    )
    company_id: Optional[str] = Field(None, description="企業ID")
    branch_id: Optional[str] = Field(None, description="店舗ID")


class UserCreate(UserBase):
    """ユーザー作成時のモデル"""

    password: str = Field(..., description="パスワード", min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "testuser",
                "password": "strongpassword123",
                "role": "user",
                "company_id": "company_123",
                "branch_id": "store_456",
                "is_active": True,
            }
        }


class UserUpdate(BaseModel):
    """ユーザー情報更新時のモデル"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    """APIレスポンス用ユーザーモデル"""

    id: str = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True
