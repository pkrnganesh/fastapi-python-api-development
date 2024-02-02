from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
   
    class Config:
        env_file = ".env"
        validate_assignment = True  # This ensures that assignments are validated

settings = Settings(

    database_port="5432",  # This is causing the issue
)
