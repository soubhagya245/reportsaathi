from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    port: int = 8000
    db_path: str = "data/reportsaathi.db"
    scratch_dir: str = "/tmp/scratch"
    data_salt: str = "test_salt_change_in_production"
    whatsapp_verify_token: str = "rep_saathi_verify_secure_token"
    whatsapp_token: str = ""
    whatsapp_phone_id: str = ""
    enable_ai_smoothing: bool = False
    local_tts_engine: str = "gtts"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
