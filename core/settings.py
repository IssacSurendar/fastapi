from pydantic import BaseSettings
import os

 
class Settings(BaseSettings):
    database_hostname : str 
    database_port : int 
    database_username : str 
    database_password : str 
    database_name : str 
    secret_key : str
    algorithm : str
    access_token_expire_minutes: int
 
    class Config:

        env_file = "/home/surendar/Desktop/fastapi/.env"


settings = Settings()