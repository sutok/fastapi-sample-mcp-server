from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings, configure_warnings
from .core.firebase import initialize_firebase
from .api.v1.endpoints import auth, users, reservations, companies, stores
import logging

# アプリケーション起動時に一度だけFirebaseを初期化
initialize_firebase()


# ロギング設定
def setup_logging():
    logging_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def create_app() -> FastAPI:
    # 警告とロギングの設定を適用
    configure_warnings()
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        description="予約管理システムのAPI",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        debug=settings.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 必要に応じて制限
        allow_credentials=True,
        allow_methods=["*"],  # ここが重要
        allow_headers=["*"],  # ここが重要
    )

    # APIルーターの設定
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    app.include_router(
        companies.router, prefix=f"{settings.API_V1_STR}/companies", tags=["companies"]
    )
    app.include_router(
        stores.router, prefix=f"{settings.API_V1_STR}/stores", tags=["stores"]
    )
    app.include_router(
        users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"]
    )
    app.include_router(
        reservations.router,
        prefix=f"{settings.API_V1_STR}/reservations",
        tags=["reservations"],
    )

    return app


app = create_app()


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
