from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    All configurable values are loaded from environment variables.
    Business logic must never read environment variables directly.
    """

    # --------------------------
    # Application
    # --------------------------
    app_name: str = "BankOpsAI"
    environment: str = "local"
    log_level: str = "INFO"

    # --------------------------
    # AI
    # --------------------------
    ai_provider: str = "openai"
    openai_api_key: str
    openai_base_url: str | None = None
    default_model: str = "gpt-5-mini"

    # --------------------------
    # Pinecone
    # --------------------------
    pinecone_api_key: str
    pinecone_index_name: str

    # --------------------------
    # LangSmith
    # --------------------------
    langsmith_api_key: str = ""
    langsmith_tracing: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()