from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from ..core.config import settings


class FirebaseAuthMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(FirebaseAuthMiddleware, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            credentials: HTTPAuthorizationCredentials = await super(
                FirebaseAuthMiddleware, self
            ).__call__(request)

            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="認証情報がありません。",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="無効な認証スキームです。",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            try:
                # Firebase Auth Emulatorを使用している場合の処理
                if settings.ENVIRONMENT == "development":
                    # エミュレータでのトークン検証ロジック
                    return {"uid": "test_uid", "email": "test@example.com"}

                # 本番環境での処理
                decoded_token = auth.verify_id_token(credentials.credentials)
                return decoded_token

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="無効な認証トークンです。",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except HTTPException as e:
            if e.status_code == 403:  # FastAPIのデフォルトの403を401に変更
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="認証情報がありません。",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            raise
