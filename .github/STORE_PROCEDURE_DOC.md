# Store Procedures Documentation

This document describes the stored procedures used in the TOEIC API system. Each procedure is stored in a separate file in the `mysql_store_procedure/` directory.


## 📋 Store Procedures List

### 1. SELECT_ALL_TEST_PROC

**📄 File:** [`SELECT_ALL_TEST_PROC.sql`](../mysql_store_procedure/SELECT_ALL_TEST_PROC.sql)

**🎯 Purpose:** Get a list of all tests with overview information

**📝 Description:**
- Returns a list of tests with `visible = 1`
- Includes part information and question count for each part
- Returns complete test structure with all 7 TOEIC parts

**🔧 Parameters:**
- `OUT pJSON_LIST_RESULT JSON` - JSON result containing the test list

**📊 JSON Response Structure:**
```json
[
  {
    "test_id": 28,
    "test_title": "Test 03",
    "test_description": "",
    "test_duration": 120,
    "part_list": [
      {
        "part_id": 62,
        "part_order": "Part 1",
        "part_title": "Listening Trial Test - Part 1",
        "total_question": 10
      },
      {
        "part_id": 63,
        "part_order": "Part 2",
        "part_title": "Listening Trial Test - Part 2",
        "total_question": 30
      },
				{
					"part_id": 65,
					"part_order": "Part 3",
					"part_title": "Listening Trial Test - Part 3",
					"total_question": 30
				},
				{
					"part_id": 66,
					"part_order": "Part 4",
					"part_title": "Listening Trial Test - Part 4",
					"total_question": 30
				},
				{
					"part_id": 67,
					"part_order": "Part 5",
					"part_title": "Reading Trial Test - Part 5",
					"total_question": 40
				},
				{
					"part_id": 68,
					"part_order": "Part 6",
					"part_title": "Reading Trial Test - Part 6",
					"total_question": 12
				},
				{
					"part_id": 69,
					"part_order": "Part 7",
					"part_title": "Reading Trial Test - Part 7",
					"total_question": 48
				}
    ]
  }
]
```

**🚀 Usage:**
```sql
CALL SELECT_ALL_TEST_PROC(@result);
SELECT @result;
```

---

### 2. SELECT_TEST_DETAIL_PROC

**📄 File:** [`SELECT_TEST_DETAIL_PROC.sql`](../mysql_store_procedure/SELECT_TEST_DETAIL_PROC.sql)

**🎯 Purpose:** Get detailed information of a specific test

**📝 Description:**
- Returns detailed information of a test by ID
- Includes all parts, media, questions and answers
- Clear hierarchical data structure with multiple media objects per part
- Provides complete test content for exam execution
- Null fields are returned as empty strings ("")
- Each media object contains question list with 4 answer choices (A, B, C, D)

**🔧 Parameters:**
- `IN pTEST_ID INT` - ID of the test to get details
- `OUT pJSON_RESULT JSON` - JSON result containing test details

**📊 JSON Response Structure:**
```json
{
  "part_list": [
    {
      "part_id": 71,
      "part_order": "Part 1",
      "part_title": "Listening Test 1 - Part 1",
      "part_audio_url": "/audio/part1.mp3",
      "media_list": [
        {
          "media_id": 558,
          "media_name": "1",
          "media_paragraph_main": "<p> base64 image </p>",
          "media_audio_script": "",
          "media_explain_question": "",
          "media_translate_script": "",
          "question_list": [
            {
              "question_id": 922,
              "question_number": 1,
              "question_content": "",
              "answer_list": [
                {
                  "answer_id": 3605,
                  "is_correct": 1,
                  "content": "A"
                },
                {
                  "answer_id": 3606,
                  "is_correct": 0,
                  "content": "B"
                },
                {
                  "answer_id": 3607,
                  "is_correct": 0,
                  "content": "C"
                },
                {
                  "answer_id": 3608,
                  "is_correct": 0,
                  "content": "D"
                }
              ]
            }
          ]
        },
        {
          "media_id": 559,
          "media_name": "2",
          "media_paragraph_main": "<p> base64 image </p>",
          "media_audio_script": "",
          "media_explain_question": "",
          "media_translate_script": "",
          "question_list": [
            {
              "question_id": 923,
              "question_number": 2,
              "question_content": "",
              "answer_list": [
                {
                  "answer_id": 3609,
                  "is_correct": 0,
                  "content": "A"
                },
                {
                  "answer_id": 3610,
                  "is_correct": 1,
                  "content": "B"
                },
                {
                  "answer_id": 3611,
                  "is_correct": 0,
                  "content": "C"
                },
                {
                  "answer_id": 3612,
                  "is_correct": 0,
                  "content": "D"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**🚀 Usage:**
```sql
CALL SELECT_TEST_DETAIL_PROC(28, @result);
SELECT @result;
```

---

## 🛠️ Deployment Guide

### 1. Create stored procedures

Execute the SQL files in order:

```bash
# In MySQL Workbench or MySQL CLI
mysql> source mysql_store_procedure/SELECT_ALL_TEST_PROC.sql
mysql> source mysql_store_procedure/SELECT_TEST_DETAIL_PROC.sql
```

### 2. Verify stored procedures

```sql
-- View procedures list
SHOW PROCEDURE STATUS WHERE Db = 'your_database_name';

-- View procedure structure
SHOW CREATE PROCEDURE SELECT_ALL_TEST_PROC;
```

### 3. Test procedures

```sql
-- Test SELECT_ALL_TEST_PROC
CALL SELECT_ALL_TEST_PROC(@all_tests);
SELECT @all_tests;

-- Test SELECT_TEST_DETAIL_PROC
CALL SELECT_TEST_DETAIL_PROC(28, @test_detail);
SELECT @test_detail;
```

## 🔄 Updates and Maintenance

- **Backup:** Always backup database before updating procedures
- **Documentation:** Update this documentation when changes occur

## 📊 TOEIC Test Structure

Each test follows the standard TOEIC format:

| Part   | Section                         | Questions | Time    | Audio |
| ------ | ------------------------------- | --------- | ------- | ----- |
| Part 1 | Listening - Photographs         | 10        | ~10 min | ✅     |
| Part 2 | Listening - Question-Response   | 30        | ~25 min | ✅     |
| Part 3 | Listening - Conversations       | 30        | ~25 min | ✅     |
| Part 4 | Listening - Short Talks         | 30        | ~25 min | ✅     |
| Part 5 | Reading - Incomplete Sentences  | 40        | ~35 min | ❌     |
| Part 6 | Reading - Text Completion       | 12        | ~25 min | ❌     |
| Part 7 | Reading - Reading Comprehension | 48        | ~75 min | ❌     |

**Total:** 200 questions, 120 minutes
