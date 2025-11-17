from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class CredentialType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"


class OtpPurpose(str, Enum):
    RESET_PASSWORD = "reset_password"
    VERIFY_ACCOUNT = "verify_account"
    VERIFY_EMAIL = "verify_email"
    VERIFY_PHONE = "verify_phone"
    TWO_FACTOR_AUTH = "two_factor_auth"


class UserRequestBase(BaseModel):
    username: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    date_joined: datetime = datetime.now()
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None


class RegisterRequest(UserRequestBase):
    password: str


class RegisterResponse(BaseModel):
  message: str
  user: UserResponse


class LoginRequest(BaseModel):
    credential: str
    password: str

    @field_validator('credential')
    @classmethod
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError('User name or email must be provided')
        return v.strip()


class TokenRequest(BaseModel):
    token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenRequest(BaseModel):
    sub: str
    user_id: str
    role: str
    token_type: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class OtpServiceRequest(BaseModel):
    credential: str
    credential_type: CredentialType
    purpose: OtpPurpose              

    @field_validator("credential")
    @classmethod
    def validate_credential(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Credential must be a string")
        if not v.strip():
            raise ValueError("Username or email is required")
        return v.strip()


class VerifyOtpServiceRequest(BaseModel):
    otp: str
    purpose: OtpPurpose


class OtpServiceResponse(BaseModel):
    success: bool
    message: str
    email_sent: bool
    expires_in_minutes: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "OTP has been sent to your email",
                "email_sent": True,
                "expires_in_minutes": 5
            }
        }


class VerifyOtpServiceResponse(BaseModel):
    success: bool
    token: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "message": "OTP verified successfully"
            }
        }


class ResetPasswordResponse(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Password reset successfully"
            }
        }