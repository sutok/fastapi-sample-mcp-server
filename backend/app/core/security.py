from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from firebase_admin import auth
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..core.config import settings
import jwt
import requests
import logging
from fastapi.security.utils import get_authorization_scheme_param

logger = logging.getLogger(__name__)


class FirebaseAuthBearer(HTTPBearer):
    """カスタムFirebase認証ベアラー"""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        認証ヘッダーを検証してクレデンシャルを返す
        """
        authorization: str = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証情報がありません。",
                headers={"WWW-Authenticate": "Bearer"},
            )

        scheme, credentials = get_authorization_scheme_param(authorization)

        if not scheme or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効な認証スキームです。Bearer認証が必要です。",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証トークンがありません。",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


# カスタム認証インスタンスを作成
firebase_auth = FirebaseAuthBearer()


class SecurityService:
    @staticmethod
    async def set_custom_claims(uid: str, claims: dict) -> None:
        """
        ユーザーのカスタムクレームを設定

        Args:
            uid (str): ユーザーID
            claims (dict): 設定するカスタムクレーム
                例: {
                    "role": "store_admin",
                    "company_id": "company_123",
                    "store_id": "store_456"
                }
        """
        try:
            # 開発環境の場合はスキップ（エミュレータではカスタムクレーム機能は利用不可）
            if settings.ENVIRONMENT == "development":
                logger.info(
                    f"Development environment: Skipping custom claims setting for uid {uid}"
                )
                return

            # 本番環境での処理
            auth.set_custom_user_claims(uid, claims)
            logger.info(f"Custom claims set for user {uid}: {claims}")
        except Exception as e:
            logger.error(f"Error setting custom claims for user {uid}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="カスタムクレームの設定に失敗しました",
            )

    @staticmethod
    async def verify_firebase_token(
        credentials: HTTPAuthorizationCredentials = Depends(firebase_auth),
    ) -> dict:
        """
        Firebaseトークンを検証し、ユーザー情報を取得
        """
        try:
            token = credentials.credentials

            # 開発環境（エミュレータ）での処理
            if settings.ENVIRONMENT == "development":
                try:
                    decoded_token = jwt.decode(
                        token, options={"verify_signature": False}
                    )
                    return {
                        "uid": decoded_token.get("user_id", "test_user_id"),
                        "email": decoded_token.get("email", "test@example.com"),
                        "email_verified": decoded_token.get("email_verified", True),
                        # 開発環境用のデフォルトのカスタムクレーム
                        "role": "store_admin",
                        "company_id": "test_company_id",
                        "store_id": "test_store_id",
                    }
                except Exception as e:
                    logger.error(f"Token verification error in emulator: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="無効なトークンです。",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

            # 本番環境での処理
            try:
                decoded_token = auth.verify_id_token(token)
                return {
                    "uid": decoded_token["uid"],
                    "email": decoded_token.get("email"),
                    "email_verified": decoded_token.get("email_verified", False),
                    # カスタムクレームを取得
                    "role": decoded_token.get(
                        "role", "user"
                    ),  # デフォルトは一般ユーザー
                    "company_id": decoded_token.get("company_id"),
                    "store_id": decoded_token.get("store_id"),
                }
            except Exception as e:
                logger.error(f"Token verification error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="無効なトークンです。",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証エラーが発生しました。",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def create_custom_token(uid: str) -> str:
        """
        カスタムトークンを作成

        Args:
            uid (str): ユーザーID

        Returns:
            str: カスタムトークン

        Raises:
            HTTPException: トークン作成に失敗した場合
        """
        try:
            return auth.create_custom_token(uid)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating custom token",
            )


# シングルトンインスタンスの作成
security_service = SecurityService()
