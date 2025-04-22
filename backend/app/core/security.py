from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from firebase_admin import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..core.config import settings
import jwt
import requests

# HTTPBearerスキームの設定
firebase_auth = HTTPBearer()


class SecurityService:
    @staticmethod
    async def verify_firebase_token(
        credentials: HTTPAuthorizationCredentials = Depends(firebase_auth),
    ) -> dict:
        """
        Firebaseトークンを検証し、ユーザー情報を取得

        Args:
            credentials: HTTPAuthorizationCredentials

        Returns:
            dict: 検証済みのユーザー情報

        Raises:
            HTTPException: トークンが無効な場合
        """
        try:
            # Bearer tokenから実際のトークンを取得
            token = credentials.credentials

            # 開発環境（エミュレータ）での処理
            if settings.ENVIRONMENT == "development":
                try:
                    # エミュレータでのトークン検証
                    # JWT自体をデコードしてユーザー情報を取得
                    decoded_token = jwt.decode(
                        token, options={"verify_signature": False}
                    )

                    # ユーザー情報をエミュレータから取得
                    auth_url = f"http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:lookup?key=fake-api-key"
                    headers = {"Content-Type": "application/json"}
                    payload = {"idToken": token}

                    response = requests.post(auth_url, json=payload, headers=headers)
                    if response.status_code == 200:
                        user_data = response.json().get("users", [{}])[0]
                        return {
                            "uid": user_data.get("localId"),
                            "email": user_data.get("email"),
                            "email_verified": user_data.get("emailVerified", False),
                        }

                    return {
                        "uid": decoded_token.get("user_id"),
                        "email": decoded_token.get("email"),
                        "email_verified": decoded_token.get("email_verified", False),
                    }
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Invalid token in emulator: {str(e)}",
                    )

            # 本番環境での処理
            decoded_token = auth.verify_id_token(token)
            return {
                "uid": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified", False),
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
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
