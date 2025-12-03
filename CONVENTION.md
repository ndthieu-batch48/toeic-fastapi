# TOEIC FastAPI Project - Coding Conventions

This document outlines the coding conventions and naming standards for the TOEIC FastAPI project. These rules apply across **all layers**: Frontend, Backend, and Database (queries, stored procedures, tables).

---

## 📝 Table of Contents

- [Naming Conventions](#-naming-conventions)
- [Database Conventions](#-database-conventions)
- [API Conventions](#-api-conventions)
- [Code Style](#-code-style)

---

## 🏗️ Naming Conventions

### **Rules of Thumb**

1. **Consistency First**: Use the same naming style across all layers
2. **Clarity Over Brevity**: Always use full words for clarity
3. **No Single Letters**: Except for loop variables and common abbreviations (id, x, y, i, j)
4. **Meaningful Names**: Names should clearly indicate their purpose and context

### **Case Styles by Layer**

| Layer                            | Style                                  | Example                                                           |
| -------------------------------- | -------------------------------------- | ----------------------------------------------------------------- |
| **Python - Variables/Functions** | `snake_case`                           | `question_id`, `get_question_detail()`, `translate_script`        |
| **Python - Classes**             | `PascalCase`                           | `QuestionDetail`, `MediaDetail`, `GeminiTranslateQuestionRequest` |
| **SQL - Tables**                 | `snake_case` with `toeicapp_` prefix   | `toeicapp_test`, `toeicapp_question`                              |
| **SQL - Columns/Alias**          | `snake_case`                           | `user_score`, `language_code`                                     |
| **SQL - Stored Procedures**      | `UPPER_SNAKE_CASE` with `_PROC` suffix | `SELECT_QUESTION_DETAIL_PROC`, `INSERT_USER_ANSWER_PROC`          |
| **SQL - Procedure Parameters**   | `pUPPER_SNAKE_CASE` (prefix `p`)       | `pQUESTION_ID`, `pLANGUAGE_ID`, `pJSON_RESULT`                    |

---

## 🗄️ Database Conventions

### **Existing Tables**

> **Important:** The following tables were created before these conventions were established. Their names **must remain unchanged** to maintain backward compatibility. However, **new columns** added to these tables and any **new tables** created must follow the naming conventions outlined in this document.

**Existing Tables (DO NOT RENAME):**
- `toeicapp_test`
- `toeicapp_testpart`
- `toeicapp_testbank`
- `toeicapp_part`
- `toeicapp_answer`
- `toeicapp_media`
- `toeicapp_history`
- `toeicapp_language`
- `toeicapp_otp`
- `toeicapp_user`

### **Table Names**
- **Prefix:** `toeicapp_` (required for all tables)
- **Style:** `snake_case`
- **No Acronyms:** Use full words for clarity
- **Form:** Singular preferred

```sql
-- ✅ Good (New Tables - Examples)
toeicapp_user_progress          -- User progress tracking
toeicapp_achievement            -- User achievements
toeicapp_notification           -- User notifications

-- ❌ Bad (New Tables)
toeicapp_user_prog              -- Don't use acronyms (use 'progress')
toeicapp_question_bookmark      -- Already in existing tables
user_progress                   -- Missing toeicapp_ prefix
toeicapp_notifications          -- Plural form (use singular)
```

### **Column/Alias Names**
- **Style:** `snake_case`
- **No Acronyms:** Use full words for clarity
- **Foreign Keys:** `{table}_id` format
- **Applies to:** ALL columns (existing and new tables)

```sql
-- ✅ Good
user_id
session_id
question_completed
answer_correct
study_duration
progress_percent
last_updated

-- ❌ Bad
question_completed     -- Already good
notificationTitle      -- Wrong case style (use snake_case)
answer_expl            -- Incomplete word (use 'answer_explanation')
userid                 -- Missing underscore separator
progress_percent       -- Already good
description            -- Already good
duration_minutes       -- Too specific, use 'duration'
```

### **Stored Procedure Names**
- **Case:** `UPPER_SNAKE_CASE`
- **Prefix:** Action verb (`SELECT_`, `INSERT_`, `UPDATE_`, `DELETE_`)
- **Suffix:** `_PROC` (required)
- **No Acronyms:** Use full words

```sql
-- ✅ Good (Examples)
SELECT_USER_PROGRESS_PROC
SELECT_QUESTION_BOOKMARK_PROC
INSERT_STUDY_SESSION_PROC
UPDATE_USER_ACHIEVEMENT_PROC
DELETE_NOTIFICATION_PROC
SELECT_QUESTION_BY_DIFFICULTY_PROC

-- ❌ Bad
select_user_progress                    -- Wrong case (must be UPPER_SNAKE_CASE)
SELECT_QUESTION_BOOKMARK_PROC           -- Already good
SELECT_USER_PROGRESS                    -- Missing _PROC suffix
GET_USER_PROGRESS_PROC                  -- Use SELECT instead of GET
SelectUserProgressProc                  -- Wrong case style (must be UPPER_SNAKE_CASE)
SELECT_USER_PROG_PROC                   -- Don't use acronyms (use 'progress')
```

### **Stored Procedure Parameters**
- **Prefix:** `p` (required)
- **Case:** `UPPER_SNAKE_CASE`
- **No Acronyms:** Use full words
- **Format:** `p{PARAMETER_NAME}`

```sql
-- ✅ Good (Examples)
CREATE PROCEDURE SELECT_USER_PROGRESS_PROC(
    IN pUSER_ID INT,
    IN pSESSION_ID INT,
    IN pSTART_DATE DATE,
    OUT pJSON_RESULT JSON
)

CREATE PROCEDURE INSERT_STUDY_SESSION_PROC(
    IN pUSER_ID INT,
    IN pQUESTION_LIST JSON,
    IN pDURATION INT,
    OUT pSESSION_ID INT,
    OUT pRESULT_STATUS VARCHAR(50)
)

CREATE PROCEDURE UPDATE_QUESTION_BOOKMARK_PROC(
    IN pUSER_ID INT,
    IN pQUESTION_ID INT,
    IN pIS_BOOKMARKED BOOLEAN,
    OUT pSUCCESS BOOLEAN
)

-- ❌ Bad
CREATE PROCEDURE SELECT_USER_PROGRESS_PROC(
    IN user_id INT,             -- Wrong case, missing prefix
    IN pSession_Id INT,         -- Wrong case (must be UPPER_SNAKE_CASE)
    IN START_DATE DATE,         -- Missing 'p' prefix
    OUT result JSON             -- Wrong case, missing 'p' prefix
)
```

---

## 🌐 API Conventions

### **Endpoint Naming**
- **Style:** `kebab-case`
- **Convention:** Follow RESTful principles
- **No Acronyms:** Use full words for clarity

```python
# ✅ Good
@router.get("/question/{question_id}")
@router.get("/test/{test_id}/part/{part_id}/detail")
@router.post("/gemini/translate/question")
@router.post("/gemini/translate/image")
@router.get("/user/{user_id}/progress")

# ❌ Bad
@router.get("/ques/{ques_id}")             # Don't use acronyms
@router.get("/getQuestionDetail")          # Not RESTful, wrong case
@router.post("/gem/trans/ques")            # Don't use acronyms
@router.get("/user/{user_id}/prog")        # Don't use acronyms (use 'progress')
```

### **Request/Response Schema Names**
- **Format:** `{Service}{Action}{Entity}{Type}`
- **Style:** `PascalCase`
- **No Acronyms:** Use full words consistently

```python
# ✅ Good
class GeminiTranslateQuestionRequest(BaseModel):
    question_id: int
    language_id: str

class GeminiTranslateQuestionResponse(BaseModel):
    question_id: int
    question_content: str
    answer_list: list[str]

class GeminiTranslateImageRequest(BaseModel):
    media_id: int
    language_id: str

class UserProgressResponse(BaseModel):
    user_id: int
    progress_percent: float
    question_completed: int

# ❌ Bad
class GemTransQuesReq(BaseModel):                    # Don't use acronyms
class TranslateRequest(BaseModel):                   # Not specific enough
class GemTransQuesRes(BaseModel):                    # Don't use acronyms
class UserProgRes(BaseModel):                        # Don't use acronyms
```

### **JSON Response Fields**
- Use snake_case
- Use full words (no acronyms)
- Match database column names when possible

```json
// ✅ Good
{
  "question_id": 1,
  "question_content": "What is...?",
  "question_number": 1,
  "answer_list": [
    {
      "answer_id": 1,
      "answer_content": "A",
      "is_correct": 1
    }
  ]
}

// ❌ Bad
{
  "questionId": 1,          // Wrong case style
  "ques_content": "...",    // Don't use acronyms
  "answerList": []          // Wrong case style
}
```

---

## 💻 Code Style

### **Python (Backend)**

#### **Import Organization**
```python
# Standard library
import json
import os
from typing import List, Optional

# Third-party
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

# Local
from app.core.gem_client import generate_text_with_gem
from app.features.test.schemas import GemTransQuesReq, GemTransQuesRes
```

#### **Function Names**
- Use snake_case
- Verb + noun pattern
- Use full words (no acronyms)

```python
# ✅ Good
async def get_question_detail(question_id: int):
async def translate_question(request: GeminiTranslateQuestionRequest):
async def stream_part_audio(test_id: int, part_id: int):

# ❌ Bad
async def getQuestionDetail(question_id: int):          # Wrong case
async def trans_ques(request):                          # Don't use acronyms
async def get_q(id: int):                               # Too short
```

#### **Variable Names**
```python
# ✅ Good
question_id = 1
question_content = "What is...?"
answer_list = []
media_paragraph_main = "<p>...</p>"
script_translate = "Dịch..."

# ❌ Bad
ques_id = 1               # Don't use acronyms
qId = 1                   # Wrong case
q = 1                     # Too short
```

### **TypeScript/JavaScript (Frontend)**

> **Note:** For complete frontend conventions, please refer to the Frontend Convention Document.

#### **Quick Reference for Backend-Frontend Integration**

When creating API schemas that will be used by frontend:

```python
# Backend schema
class GeminiTranslateQuestionRequest(BaseModel):
    question_id: int
    language_id: str

# Frontend will receive/send as (camelCase):
# {
#   "questionId": 1,
#   "languageId": "vi"
# }
```

---

## 📋 Quick Reference

### **Naming Checklist**

Before naming anything, ask:
1. ✅ Am I using the correct case style for this layer?
2. ✅ Are all words spelled out in full (no acronyms)?
3. ✅ Am I using consistent naming across all layers?
4. ✅ Is the name clear and descriptive?

### **Database Quick Reference**

| Element           | Format                         | Example                                                |
| ----------------- | ------------------------------ | ------------------------------------------------------ |
| Existing Tables   | `toeicapp_{name}` (keep as is) | `toeicapp_test`, `toeicapp_user`, `toeicapp_media`     |
| New Tables        | `toeicapp_{name}` (full words) | `toeicapp_user_progress`, `toeicapp_question_bookmark` |
| All Columns       | `snake_case` (full words)      | `user_id`, `question_completed`, `script_translate`    |
| Stored Procedures | `ACTION_NAME_PROC`             | `SELECT_USER_PROGRESS_PROC`                            |
| Procedure Params  | `pUPPER_CASE`                  | `pUSER_ID`, `pQUESTION_ID`, `pJSON_RESULT`             |

---

## 🔄 Migration Guide

When refactoring existing code to follow these conventions:

1. **Start with new features** - Apply conventions to all new code
2. **Update schemas first** - Change request/response models
3. **Update database layer** - Modify column names in new tables
4. **Update API endpoints** - Keep backward compatibility if needed
5. **Document changes** - Update API documentation

---

**Last Updated:** December 3, 2025  
**Maintained by:** Development Team