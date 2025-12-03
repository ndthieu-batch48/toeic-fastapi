
## Project Structure

```
toeic-fastapi/
├── README.md
├── main.py
├── requirements.txt
├── run_fastapi.bat
├── venv/
│
├── app/
│   ├── api_router.py
│   ├── app.py
│   │
│   ├── core/
│   │   ├── app_config.py
│   │   ├── gemini_client.py
│   │   ├── mysql_connection.py
│   │   └── smtp_config.py
│   │
│   ├── features/
│   │   ├── auth/
│   │   │   ├── auth_dependencies.py
│   │   │   ├── auth_router.py
│   │   │   ├── auth_smtp_service.py
│   │   │   ├── auth_query.py
│   │   │   ├── auth_schemas.py
│   │   │   ├── const/
│   │   │   │   └── email_const.py
│   │   │   └── helper/
│   │   │       ├── jwt_helper.py
│   │   │       └── otp_helper.py
│   │   │
│   │   ├── history/
│   │   │   ├── history_query.py
│   │   │   ├── history_router.py
│   │   │   └── history_schemas.py
│   │   │
│   │   └── test/
│   │       ├── test_audio_util.py
│   │       ├── test_const.py
│   │       ├── test_prompt_helper.py
│   │       ├── test_query.py
│   │       ├── test_router.py
│   │       └── test_schemas.py
│   │
│   └── util/
│       └── languge_util.py
│
└── mysql_store_procedure/
    ├── SELECT_ALL_TEST_PROC.sql
    └── SELECT_TEST_DETAIL_PROC.sql
```
