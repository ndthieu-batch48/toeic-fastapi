import asyncio
from fastapi import APIRouter, HTTPException, status

from .auth_schema import (
    OtpPurpose, 
    OtpServiceRequest, 
    OtpServiceResponse, 
    VerifyOtpServiceRequest,
    ResetPasswordRequest, 
    ResetPasswordResponse,
    LoginRequest, 
    UserResponse, 
    RegisterRequest,  
    RegisterResponse, 
    TokenRequest, 
    TokenResponse,
    VerifyOtpServiceResponse,
)
from ...core.mysql_connection import get_db_cursor
from .auth_query import (
    INSERT_USER, 
    SELECT_USER_BY_ID, 
    SELECT_USER_BY_EMAIL_OR_USERNAME, 
    SELECT_VALID_USER_OTP, 
    UPDATE_USER_OTP,
    CLEAR_USER_OTP, 
    UPDATE_USER_PASSWORD_BY_ID, 
)
from ...core.app_config import app_config

from .auth_smtp_service import (
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


@router.post("/register", response_model=RegisterResponse)
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


@router.put("/password/reset", response_model=ResetPasswordResponse)
async def reset_password(req: ResetPasswordRequest):
    try:
        print(req.token)
        with get_db_cursor() as cursor:
            payload = verify_otp_action_token(req.token)
            if (payload.get("purpose") != OtpPurpose.RESET_PASSWORD.value):
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
            
            # Delete OTP after successful password reset
            cursor.execute(CLEAR_USER_OTP, (user_id,))
            
        return {"message": "Password reset successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred in reset password controller",
                "error": str(e)
            }
        )


@router.post("/password/otp", response_model=OtpServiceResponse)
async def request_password_reset_otp(req: OtpServiceRequest):
    otp, otp_expire_time = generate_expire_otp_helper()
    
    try:
        credential = None
        email_sent = False
    
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_USER_BY_EMAIL_OR_USERNAME, (req.credential, req.credential))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user_id = user.get("id")
            credential = user.get(req.credential_type.value)
            
            # Delete old unused OTP (clear previous OTP)
            cursor.execute(CLEAR_USER_OTP, (user_id,))
            
            # Update user table with new OTP
            cursor.execute(
                UPDATE_USER_OTP, 
                (otp, req.purpose.value, otp_expire_time, user_id)
            )
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate OTP"
                )

        # Send email asynchronously
        try:
            expire_display = f"{app_config.OTP_EXPIRES_MINUTES}"
            msg = build_password_reset_email(credential, otp, expire_display)
            
            # Wait for email sending to complete
            await send_email_service_async(msg)
            email_sent = True
            
        except Exception as email_error:
            # If email fails, clean up OTP
            with get_db_cursor() as cursor:
                cursor.execute(CLEAR_USER_OTP, (user_id,))
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Failed to send OTP email",
                    "error": str(email_error)
                }
            )
        
        return {
            "success": True,
            "message": f"OTP has been sent to your {req.credential_type.value}",
            "email_sent": email_sent,
            "expires_in_minutes": app_config.OTP_EXPIRES_MINUTES
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "Error in OTP request controller",
                "error": str(e)
            }
        )


@router.post("/password/otp/verify", response_model=VerifyOtpServiceResponse)
async def verify_password_reset_otp(req: VerifyOtpServiceRequest):
    try:
        user_id = None
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_VALID_USER_OTP, (req.otp, req.purpose.value))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid or expired OTP"
                )

            user_id = user.get("id")
            
            # Delete OTP after verification (Update all OTP columns to NULL)
            cursor.execute(CLEAR_USER_OTP, (user_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to process OTP verification"
                )
        
        reset_password_token = generate_otp_purpose_token(user_id, req.purpose.value)
        
        return {
            "success": True,
            "token": reset_password_token,
            "message": "OTP verified successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "Error in OTP verify controller",
                "error": str(e)
            }
        )