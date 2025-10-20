import asyncio
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .auth_schemas import (
    RegisterRequest, LoginRequest, UserResponse, TokenRequest, TokenResponse,
    ResetPasswordRequest, OtpServiceRequest, VerifyOtpServiceRequest
)
from ...core.mysql_connection import get_db_cursor
from .auth_query import (
    SELECT_USER_BY_EMAIL_OR_USERNAME, INSERT_USER, SELECT_USER_BY_ID,
    UPDATE_USER_PASSWORD_BY_ID, DELETE_UNUSED_OTP, INSERT_OTP,
    SELECT_VALID_OTP, UPDATE_USED_OTP
)
from ...core.app_config import app_config

from .smtp import (
    build_password_reset_email, 
    send_email_service_async)
from .helper.otp_helper import (
    generate_expire_otp_helper,
    generate_otp_purpose_token,
    verify_otp_action_token )
from .helper.jwt_helper import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    verify_token)

router = APIRouter()


@router.post("/register")
async def register(req: RegisterRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_USER_BY_EMAIL_OR_USERNAME, (req.email, req.username))
            existing_user = cursor.fetchone()
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Username already taken")

            hashed_password = hash_password(req.password)
            cursor.execute(INSERT_USER, (req.username, req.email,  hashed_password))
            
            user_id = cursor.lastrowid
            
            cursor.execute(SELECT_USER_BY_ID, (user_id,))
            new_user = cursor.fetchone()
            
            token_data={
                    "sub": new_user.get("username"), 
                    "user_id": new_user.get("id"), 
                    "role": new_user.get("role")
                }
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)
            
            response = UserResponse(
                id=new_user.get("id"), 
                email=new_user.get("email"),
                username=new_user.get("username"), 
                role=new_user.get("role"),
                date_joined=new_user.get("date_joined"), 
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
            
            return {
                "message": "User created successfully",
                "user": response
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred in register controller",
                "error": str(e),
            },
        )


@router.post("/login", response_model = UserResponse)
async def login(req: LoginRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_USER_BY_EMAIL_OR_USERNAME, (req.credential, req.credential))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found!",
                )
            
            if not verify_password(req.password, user.get("password")):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid username or password!",
                )
                
            token_data={
                    "sub": user.get("username"), 
                    "user_id": user.get("id"), 
                    "role": user.get("role")
                }
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)
            
            response = UserResponse(
                id=user.get("id"), 
                email=user["email"],
                username=user.get("username"), 
                role=user.get("role"),
                date_joined=user.get("date_joined"), 
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
            return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred in login controller",
                "error": str(e),
            },
        )


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(req: TokenRequest):
    try:
        payload = verify_token(req.token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = {
            "sub": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "role": payload.get("role"),
        }
        access_token = create_access_token(token_data)
        refresh_token_new = create_refresh_token(token_data)
        
        response = {
            "access_token": access_token,
            "refresh_token": refresh_token_new,
            "token_type": "bearer",
        }
        return response 

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred in login controller",
                "error": str(e),
            },
        )


@router.put("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    try:
        print(req.token)
        with get_db_cursor() as cursor:
            payload = verify_otp_action_token(req.token)
            if (payload.get("purpose") != "reset_password"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or mismatched token purpose.",
                )
            user_id = payload.get("sub")  
            
            cursor.execute(SELECT_USER_BY_ID, (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            if len(req.new_password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password must be at least 6 characters long"
                )
            hashed_password = hash_password(req.new_password)
            cursor.execute(UPDATE_USER_PASSWORD_BY_ID, (hashed_password, user_id))
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update password"
                )
        return {"message": "Password reset successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred in reset password controller",
                "error": {e}
            }
        )


@router.post("/otp/request")
async def send_reset_password_otp(req: OtpServiceRequest):    
    otp, otp_expire_time = generate_expire_otp_helper()
    try:
        credential = None
    
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_USER_BY_EMAIL_OR_USERNAME, (req.credential_value, req.credential_value))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user_id = user.get("id")
            credential = user.get(req.credential_type) # Get user credential base on request type: email | phone
            cursor.execute(DELETE_UNUSED_OTP, (user_id, req.purpose,))
            cursor.execute(INSERT_OTP, (otp, req.purpose, otp_expire_time, req.credential_type, req.credential_value, user_id))

        #TODO: Utilizing credential_type for different Email/SMS service
        expire_display = f"{app_config.OTP_EXPIRES_MINUTES}"
        msg = build_password_reset_email(credential, otp, expire_display)
        asyncio.create_task(send_email_service_async(msg))
        
        return {"message": "A password reset OTP will be sent to your email"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "Error in OTP request controller",
                "error": {e}
            }
        )


@router.post("/otp/verify")
async def verify_reset_password_otp(req: VerifyOtpServiceRequest):    
    try:
        user_id = None
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_VALID_OTP, (req.otp, req.purpose))
            data = cursor.fetchone()
            if not data:
                raise HTTPException(status_code=400, detail="Invalid or expired OTP")

            user_id = data.get("user_id")
            cursor.execute(UPDATE_USED_OTP, (user_id, req.otp, req.purpose))
        
        reset_password_token =  generate_otp_purpose_token(user_id, req.purpose)
        
        return JSONResponse(
            status_code=200,
            content={
                "token": reset_password_token,
                "message": "OTP is verified"
                }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "Error in OTP verify controller",
                "error": {e}
            }
        )
