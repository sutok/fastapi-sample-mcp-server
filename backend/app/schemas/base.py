from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """全てのスキーマの基底クラス"""

    created_at: Optional[datetime] = Field(None, description="作成日時")
    updated_at: Optional[datetime] = Field(None, description="更新日時")

    model_config = {
        "from_attributes": True  # Config classは非推奨になったため、model_configを使用
    }
