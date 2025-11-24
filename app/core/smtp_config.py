from pydantic_settings import BaseSettings 

class SmtpConfig(BaseSettings):
    EMAIL_SENDER: str = ""
    EMAIL_PASSCODE: str = ""
    EMAIL_SMTP_SERVER: str = "smtp.tma.com.vn"
    EMAIL_SMTP_PORT: int = 465
        
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

smtp_config = SmtpConfig()