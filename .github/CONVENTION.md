# TOEIC FastAPI Project - Coding Conventions

This document outlines the coding conventions and naming standards for the TOEIC FastAPI project. These rules apply across **all layers**: Frontend, Backend, and Database (queries, stored procedures, tables).

---

## 📝 Table of Contents

- [Acronym Rules](#-acronym-rules)
- [Naming Conventions](#-naming-conventions)
- [Database Conventions](#-database-conventions)
- [API Conventions](#-api-conventions)
- [Code Style](#-code-style)

---

## 🔤 Acronym Rules

### **Core Principle**

If a word has more than **6 characters**, **CONSIDER** using an acronym.

**Acronym Requirements:**
- **MUST** be between 3-6 characters in length
- **MUST** allow contributors to easily guess its meaning
- **MUST** be carefully reviewed before adoption
- **MUST** be added to the Standard Acronyms table below

Once an acronym is added to the table, it becomes **standard** and should be used consistently throughout the project.

### **Standard Acronyms (Current Project)**

> **Note:** This table is actively maintained and updated as the project evolves. All acronyms listed here are approved for use.

| Full Word   | Acronym   | Example Usage                                 |
| ----------- | --------- | --------------------------------------------- |
| Question    | `Ques`    | `ques_id`, `ques_content`, `GemTransQuesReq`  |
| Response    | `Resp`    | `GeminiTransQuesResp`, `TestDetailResp`       |
| Request     | `Req`     | `CreateUserReq`                               |
| Translate   | `Trans`   | `trans_script`, `media_trans_script`          |
| Language    | `Lang`    | `lang_id`, `lang_code`                        |
| Image       | `Img`     | `img_data`, `media_img`                       |
| Answer      | `Ans`     | `ans_id`, `ans_list`                          |
| Paragraph   | `Parag`   | `parag_main`, `media_parag_main`              |
| Progress    | `Prog`    | `user_prog`, `prog_percent`, `prog_tracking`  |
| Credential  | `Creden`  | `user_creden`, `creden_type`, `update_creden` |
| Description | `Descrip` | `test_descrip`, `media_descrip`               |
| Duration    | `Dura`    | `test_dura`, `session_dura`, `study_dura`     |
| Result      | `Res`     | `test_res`, `res_score`, `user_res`           |
| Option      | `Opt`     | `opt_id`, `ques_opt`, `config_opt`            |

### **Acronym Application Examples**

#### ✅ **Correct Usage**

```python
# Backend
class GemTransQuesReq(BaseModel):
    ques_id: int
    lang_id: LangCode

class GemTransQuesRes(BaseModel):
    ques_id: int
    ques_content: str
    ans_list: list[str]
    lang_id: LangCode

class MediaQuesDetailRes(BaseModel):
    media_id: int
    media_name: str
    media_para_main: str
    audio_script: Optional[str] = None
    ques_explain: Optional[str] = None
    script_trans: Optional[str] = None
    ques_list: List[QuesDetail]

# Database - Table Columns
SELECT 
    q.id AS ques_id,
    q.content AS ques_content,
    a.content AS ans_content,
    m.paragrap_main AS para_main

```

#### ❌ **Incorrect Usage**

```python
# DON'T - Mixing full words and acronyms inconsistently
class GeminiTranslateQuestionRequest(BaseModel):  # Too long, not using acronyms
    question_id: int  # Inconsistent: should use 'ques_id' (see Standard Acronyms table)
    lang_id: LanguageCode  # Mixing styles: 'question_id' vs 'lang_id'

# DON'T - Using non-standard acronyms
class GemTrQReq(BaseModel):  # "Tr" is not in Standard Acronyms table
    q_id: int  # "q" is too short (acronyms must be 3-6 characters)
    lg_id: str  # "lg" is not in Standard Acronyms table (use 'lang')
```

---

## 🏗️ Naming Conventions

### **Rules of Thumb**

> **Important:** Before applying these rules, always refer to the [Acronym Rules](#-acronym-rules) section above to determine if a word should be abbreviated. Then apply the appropriate case style from the [Case Styles by Layer](#case-styles-by-layer) table below.

1. **Consistency First**: Use the same naming style across all layers
2. **Clarity Over Brevity**: Only abbreviate words with more than 6 characters
3. **No Single Letters**: Except for loop variables and common abbreviations (id, x, y, i, j)
4. **Meaningful Names**: Names should clearly indicate their purpose and context

### **Case Styles by Layer**

| Layer                            | Style                                  | Example                                           |
| -------------------------------- | -------------------------------------- | ------------------------------------------------- |
| **Python - Variables/Functions** | `snake_case`                           | `ques_id`, `get_ques_detail()`, `trans_script`    |
| **Python - Classes**             | `PascalCase`                           | `QuesDetail`, `MediaDetail`, `GemTransQuesReq`    |
| **SQL - Tables**                 | `snake_case` with `toeicapp_` prefix   | `toeicapp_test`, `toeicapp_newtable`              |
| **SQL - Columns/Alias**          | `snake_case`                           | `user_score`, `lang_code`                         |
| **SQL - Stored Procedures**      | `UPPER_SNAKE_CASE` with `_PROC` suffix | `SELECT_QUES_DETAIL_PROC`, `INSERT_USER_ANS_PROC` |
| **SQL - Procedure Parameters**   | `pUPPER_SNAKE_CASE` (prefix `p`)       | `pQUES_ID`, `pLANG_ID`, `pJSON_RESULT`            |

---

## 🗄️ Database Conventions

### **Existing Tables**

> **Important:** The following tables were created before these conventions were established. Their names **must remain unchanged** to maintain backward compatibility. However, **new columns** added to these tables and any **new tables** created must follow the acronym conventions outlined in this document.

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
- **Acronyms:** Use approved acronyms for words > 6 characters
- **Form:** Singular preferred

```sql
-- ✅ Good (New Tables - Examples)
toeicapp_user_prog          -- User progress tracking
toeicapp_achievement        -- User achievements (Consider using an acronym -> achiev or something)
toeicapp_notification       -- User notifications (Consider using an acronym)

-- ❌ Bad (New Tables)
toeicapp_user_progress      -- Not using acronym (progress → prog)
toeicapp_question_bookmark  -- Not using acronym (question → ques)
user_prog                   -- Missing toeicapp_ prefix
toeicapp_notifications      -- Plural form (use singular)
prog_tracking               -- Missing toeicapp_ prefix
```

### **Column/Alias Names**
- **Style:** `snake_case`
- **Acronyms:** Use approved acronyms for words > 6 characters
- **Foreign Keys:** `{table}_id` format
- **Applies to:** ALL columns (existing and new tables)

```sql
-- ✅ Good
user_id
session_id
ques_completed
ans_correct
study_dura
prog_percent
last_updated

-- ❌ Bad
question_completed      -- Not using acronym (question → ques)
notificationTitle       -- Wrong case style (use snake_case)
answer_expl            -- Inconsistent acronym (use 'explanation' in full or approved acronym)
userid                 -- Missing underscore separator
progress_percent       -- Not using acronym (progress → prog)
description            -- Not using acronym (description → desc)
duration_minutes       -- Not using acronym (duration → dura)
```

### **Stored Procedure Names**
- **Case:** `UPPER_SNAKE_CASE`
- **Prefix:** Action verb (`SELECT_`, `INSERT_`, `UPDATE_`, `DELETE_`)
- **Suffix:** `_PROC` (required)
- **Acronyms:** Use approved acronyms

```sql
-- ✅ Good (Examples)
SELECT_USER_PROG_PROC
SELECT_QUES_BOOKMARK_PROC
INSERT_STUDY_SESSION_PROC
UPDATE_USER_ACHIEVEMENT_PROC
DELETE_NOTIFICATION_PROC
SELECT_QUES_BY_DIFFICULTY_PROC

-- ❌ Bad
select_user_prog                    -- Wrong case (must be UPPER_SNAKE_CASE)
SELECT_QUESTION_BOOKMARK_PROC       -- Not using acronym (question → ques)
SELECT_USER_PROG                    -- Missing _PROC suffix
GET_USER_PROG_PROC                  -- Use SELECT instead of GET
SelectUserProgProc                  -- Wrong case style (must be UPPER_SNAKE_CASE)
SELECT_USER_PROGRESS_PROC           -- Not using acronym (progress → prog)
```

### **Stored Procedure Parameters**
- **Prefix:** `p` (required)
- **Case:** `UPPER_SNAKE_CASE`
- **Acronyms:** Use approved acronyms
- **Format:** `p{PARAMETER_NAME}`

```sql
-- ✅ Good (Examples)
CREATE PROCEDURE SELECT_USER_PROG_PROC(
    IN pUSER_ID INT,
    IN pSESSION_ID INT,
    IN pSTART_DATE DATE,
    OUT pJSON_RESULT JSON
)

CREATE PROCEDURE INSERT_STUDY_SESSION_PROC(
    IN pUSER_ID INT,
    IN pQUES_LIST JSON,
    IN pDURA INT,
    OUT pSESSION_ID INT,
    OUT pRESULT_STATUS VARCHAR(50)
)

CREATE PROCEDURE UPDATE_QUES_BOOKMARK_PROC(
    IN pUSER_ID INT,
    IN pQUES_ID INT,
    IN pIS_BOOKMARKED BOOLEAN,
    OUT pSUCCESS BOOLEAN
)

-- ❌ Bad
CREATE PROCEDURE SELECT_USER_PROG_PROC(
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
- **Acronyms:** Use approved acronyms in URL paths

```python
# ✅ Good
@router.get("/ques/{ques_id}")
@router.get("/test/{test_id}/part/{part_id}/detail")
@router.post("/gem/trans/ques")
@router.post("/gem/trans/img")
@router.get("/user/{user_id}/prog")

# ❌ Bad
@router.get("/question/{question_id}")     # Not using acronym (question → ques)
@router.get("/getQuestionDetail")           # Not RESTful, wrong case
@router.post("/gemini-translate-question")  # Too long, not using acronyms
@router.get("/user/{user_id}/progress")    # Not using acronym (progress → prog)
```
@router.post("/gemini-translate-question")  # Too long
```

### **Request/Response Schema Names**
- **Format:** `{Service}{Action}{Entity}{Type}`
- **Style:** `PascalCase`
- **Acronyms:** Use approved acronyms consistently

```python
# ✅ Good
class GemTransQuesReq(BaseModel):
    ques_id: int
    lang_id: LanguageCode

class GemTransQuesRes(BaseModel):
    ques_id: int
    ques_content: str
    ans_list: list[str]

class GemTransImgReq(BaseModel):
    media_id: int
    lang_id: LanguageCode

class UserProgRes(BaseModel):
    user_id: int
    prog_percent: float
    ques_completed: int

# ❌ Bad
class GeminiTranslateQuestionRequest(BaseModel):  # Too long, not using acronyms
class TranslateRequest(BaseModel):                # Not specific enough
class QuestionTranslationRequest(BaseModel):      # Inconsistent naming style
class UserProgressResponse(BaseModel):            # Not using acronym (progress → prog)
```

### **JSON Response Fields**
- Use snake_case
- Use acronyms consistently
- Match database column names when possible

```json
// ✅ Good
{
  "ques_id": 1,
  "ques_content": "What is...?",
  "ques_number": 1,
  "ans_list": [
    {
      "ans_id": 1,
      "ans_content": "A",
      "is_correct": 1
    }
  ]
}

// ❌ Bad
{
  "questionId": 1,          // Wrong case style
  "question_content": "...", // Inconsistent acronym usage
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
- Use acronyms

```python
# ✅ Good
async def get_ques_detail(ques_id: int):
async def trans_ques(req: GemTransQuesReq):
async def stream_part_audio(test_id: int, part_id: int):

# ❌ Bad
async def getQuestionDetail(question_id: int):  # Wrong case
async def translate_question(request: GeminiTranslateQuestionRequest):  # Too long
async def get_q(id: int):  # Too short
```

#### **Variable Names**
```python
# ✅ Good
ques_id = 1
ques_content = "What is...?"
ans_list = []
media_para_main = "<p>...</p>"
script_trans = "Dịch..."

# ❌ Bad
question_id = 1  # Not using acronym
qId = 1          # Wrong case
q = 1            # Too short
```

### **TypeScript/JavaScript (Frontend)**

> **Note:** For complete frontend conventions, please refer to the Frontend Convention Document.

#### **Quick Reference for Backend-Frontend Integration**

When creating API schemas that will be used by frontend:

```python
# Backend schema
class GemTransQuesReq(BaseModel):
    ques_id: int
    lang_id: str

# Frontend will receive/send as (camelCase):
# {
#   "quesId": 1,
#   "langId": "vi"
# }
```

---

## 📋 Quick Reference

### **Acronym Checklist**

Before naming anything, ask:
1. ✅ Is the word longer than 6 characters?
2. ✅ Is there a standard acronym in our list?
3. ✅ Am I using it consistently across all layers?
4. ✅ Is the case style correct for this layer?

### **Database Quick Reference**

| Element           | Format                           | Example                                            |
| ----------------- | -------------------------------- | -------------------------------------------------- |
| Existing Tables   | `toeicapp_{name}` (keep as is)   | `toeicapp_test`, `toeicapp_user`, `toeicapp_media` |
| New Tables        | `toeicapp_{name}` (use acronyms) | `toeicapp_user_progress`, `toeicapp_ques_bookmark` |
| All Columns       | `snake_case` (use acronyms)      | `user_id`, `ques_completed`, `script_trans`        |
| Stored Procedures | `ACTION_NAME_PROC`               | `SELECT_USER_PROGRESS_PROC`                        |
| Procedure Params  | `pUPPER_CASE`                    | `pUSER_ID`, `pQUES_ID`, `pJSON_RESULT`             |

---

## 🔄 Migration Guide

When refactoring existing code to follow these conventions:

1. **Start with new features** - Apply conventions to all new code
2. **Update schemas first** - Change request/response models
3. **Update database layer** - Modify column names in new tables
4. **Update API endpoints** - Keep backward compatibility if needed
5. **Document changes** - Update API documentation

---

## 📞 Questions?

If you encounter a word not in the acronym list:
1. Check if it's ≤ 6 characters (keep it full)
2. If > 6 characters, propose a standard acronym
3. Update this document
4. Ensure team consensus before using

---

**Last Updated:** October 15, 2025  
**Maintained by:** Development Team