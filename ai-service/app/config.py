from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    internal_api_secret: str = "change-me"
    groq_api_key: str = ""
    groq_model: str = ""
    vision_provider: str = "hosted"
    vision_model: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    vision_api_base_url: str = ""
    vision_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
