"""User and authentication related queries"""

SELECT_USER_BY_EMAIL_OR_USERNAME = "SELECT * FROM toeicapp_user WHERE email = %s OR username = %s"


SELECT_USER_BY_EMAIL = "SELECT * FROM toeicapp_user WHERE email = %s"


INSERT_USER = "INSERT INTO toeicapp_user (username, email, password) VALUES (%s, %s, %s)"


SELECT_USER_BY_ID = """
    SELECT *
    FROM toeicapp_user
    WHERE id = %s
"""


UPDATE_USER_IS_VERIFIED = """
    UPDATE TABLE toeicapp_user
    SET is_verified = 1
    WHERE email = %s;
"""


UPDATE_USER_OTP = """
    UPDATE toeicapp_user 
    SET otp = %s, 
        otp_purpose = %s, 
        otp_is_used = 0,
        otp_expire_at = %s,
        otp_created_at = NOW()
    WHERE id = %s;
"""


SELECT_VALID_USER_OTP = """
    SELECT * FROM toeicapp_user 
    WHERE otp = %s 
    AND otp_purpose = %s 
    AND otp_is_used = 0 
    AND otp_expire_at > NOW();
"""


# Delete OTP from user (set to NULL)
CLEAR_USER_OTP = """
    UPDATE toeicapp_user
    SET otp = NULL,
        otp_purpose = NULL,
        otp_is_used = NULL,
        otp_expire_at = NULL,
        otp_created_at = NULL
    WHERE id = %s;
"""


UPDATE_USER_PASSWORD_BY_ID = """ 
    UPDATE toeicapp_user 
    SET password = %s
    WHERE id = %s
"""



