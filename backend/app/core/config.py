from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "HireMeAI API"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://hiremeai:change_me@localhost:5432/hiremeai"
    clerk_jwks_url: str = ""
    clerk_issuer: str = ""
    clerk_authorized_parties: str = "http://localhost:3000"
    ai_service_url: str = "http://localhost:8001"
    internal_api_secret: str = "change-me"
    s3_endpoint_url: str = "http://localhost:9000"
    s3_bucket: str = "hiremeai-files"
    s3_access_key: str = "hiremeai_app"
    s3_secret_key: str = "change-me"
    s3_region: str = "us-east-1"
    max_upload_mb: int = 8
    frontend_url: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def authorized_parties(self) -> list[str]:
        return [item.strip() for item in self.clerk_authorized_parties.split(",") if item.strip()]

settings = Settings()
