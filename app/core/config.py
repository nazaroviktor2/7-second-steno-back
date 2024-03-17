from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DESCRIPTION: str = "7s backend"
    SERVICE_NAME: str = "7s backend"
    API_PATH: str = "/api"
    API_VERSION: str = "v1"
    DEBUG: bool = True

    IS_CELERY_APP: bool = False

    MINIO_ENDPOINT: str
    MINIO_LOGIN: str
    MINIO_PASS: str
    MINIO_BUCKET: str = "s7-files"

    CELERY_BROKER_URL: str
    TASK_ALWAYS_EAGER: bool = False

    POSTGRES_URI: str

    SEARCH_ENGINE_HOST: str
    SEARCH_ENGINE_LOGIN: str
    SEARCH_ENGINE_PASSWORD: str

    AVAILABLE_FILE_TYPE: dict = {
        "audio/mpeg": "mp3",
    }

    HF_TOKEN: str

    MAX_SIZE: int = 3787631740


config = Config()
