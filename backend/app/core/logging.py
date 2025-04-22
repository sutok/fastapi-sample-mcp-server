import logging
from logging.config import dictConfig
from .config import settings

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        }
    },
}

dictConfig(logging_config)
logger = logging.getLogger("app")


def setup_custom_logging():
    # ルートロガーの設定
    logger = logging.getLogger()

    # 既存のハンドラをクリア
    logger.handlers.clear()

    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()

    # フォーマッターの設定
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # ログレベルの設定
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # ハンドラの追加
    logger.addHandler(console_handler)

    # Firestoreの警告を制御
    if not settings.DEBUG:
        logging.getLogger("google.cloud.firestore_v1").setLevel(logging.WARNING)
