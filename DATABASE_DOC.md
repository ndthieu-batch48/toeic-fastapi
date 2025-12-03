# DATABASE DOCUMENTATION

This documentation describes the table designs in the TOEIC application database. Note: Some columns and tables are currently unused; you can ignore them for now or use them in the future.

## 1. toeicapp_user

**Purpose:** Store user account data and OTP (one-time password) information.

**Unused columns:** `date_joined`, `role`

| Field          | Type         | Null | Key | Default           | Extra             |
| -------------- | ------------ | ---- | --- | ----------------- | ----------------- |
| id             | bigint       | NO   | PRI |                   | auto_increment    |
| username       | varchar(150) | NO   | UNI |                   |                   |
| email          | varchar(254) | NO   | UNI |                   |                   |
| password       | varchar(255) | NO   |     |                   |                   |
| date_joined    | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| role           | varchar(255) | NO   |     | student           |                   |
| is_verified    | tinyint(1)   | YES  |     | 0                 |                   |
| otp            | varchar(10)  | YES  |     |                   |                   |
| otp_purpose    | varchar(50)  | YES  |     |                   |                   |
| otp_is_used    | tinyint(1)   | YES  |     |                   |                   |
| otp_expire_at  | timestamp    | YES  |     |                   |                   |
| otp_created_at | timestamp    | YES  |     |                   |                   |

---

## 2. toeicapp_test

**Purpose:** Store TOEIC test data. Only tests with `visible = 1` will be displayed to users.

**Unused columns:** `test_bank_id`, `test_type`

| Field        | Type         | Null | Key | Default | Extra          |
| ------------ | ------------ | ---- | --- | ------- | -------------- |
| id           | bigint       | NO   | PRI |         | auto_increment |
| title        | varchar(255) | NO   |     |         |                |
| description  | longtext     | YES  |     |         |                |
| duration     | int unsigned | NO   |     |         |                |
| exam_date    | datetime(6)  | NO   |     |         |                |
| test_bank_id | bigint       | NO   | MUL |         |                |
| test_type    | varchar(10)  | NO   |     |         |                |
| visible      | tinyint(1)   | YES  |     | 1       |                |

---

## 3. toeicapp_media

**Overview**

This is a crucial table that stores all media content for TOEIC questions. Think of it as a "content container" that holds images, text passages, and audio scripts referenced by questions.

**Main Purpose**

- Store base64-encoded image data for Parts 1, 3, and 4; or passages (as text or base64 image) for Parts 6 and 7
- Store these data in the `paragrap_main` column
- Store English transcripts of audio files in the `audio_script` column

**How It Works**

- Each media record represents one content unit: a single image (Parts 1, 3, 4), a full passage (Parts 6, 7), or an audio transcript
- Multiple questions can reference the same media using the `media_group_id` field in the `toeicapp_question` table
- **Example:** A Part 3 audio conversation might have 3 questions, all pointing to the same media record

**Key Points to Remember**

- One media record = One content block (image, passage, or audio script)
- Multiple questions can use the same media (they all share the same `media_group_id`)
- The actual content lives in `paragrap_main` (image or passage text)
- Use `media_group_id` in questions to connect them to their media
- Every media record must belong to a specific test (via `test_id`)


**Unused columns:** `create_at`

| Field         | Type     | Null | Key | Default           | Extra             |
| ------------- | -------- | ---- | --- | ----------------- | ----------------- |
| id            | bigint   | NO   | PRI |                   | auto_increment    |
| paragrap_main | longtext | YES  |     |                   |                   |
| media_name    | longtext | YES  |     |                   |                   |
| test_id       | bigint   | YES  | MUL |                   |                   |
| audio_script  | longtext | YES  |     |                   |                   |
| create_at     | datetime | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

---

### Example Scenarios

This section shows practical examples of `toeicapp_media` responses across TOEIC parts. A single media record can contain one or multiple questions, depending on the part. A passage can be either **text** or **an image**.

**TOEIC Parts Relevant to Media**

| Part   | Typical media form         | Typical questions per media |
| ------ | -------------------------- | --------------------------- |
| Part 1 | Image                      | 1                           |
| Part 3 | Passage (text or image)    | multiple (commonly 3)       |
| Part 4 | Passage (text or image)    | multiple (commonly 3)       |
| Part 6 | Passage (text or image)    | multiple (commonly 4)       |
| Part 7 | Passage(s) (text or image) | multiple (1–6+)             |

> **Note:** Part 1 always has one image and one question. Parts 3, 4, 6, and 7 may use either image-based or text-based passages.

**Common Response Fields**

```json
{
  "media_question_id": <number>,
  "media_question_name": "<label or question range>",
  "media_question_main_paragraph": "image or text passage",
  "question_list": [
    {
      "question_id": <number>,
      "question_number": <number>,
      "question_content": "<string>",
      "answer_list": [
        { "answer_id": <number>, "content": "<answer text>", "is_correct": <boolean> }
      ]
    }
  ]
}
```

#### Scenario 1: Part 1 (Image + 1 Question)

```json
{
  "media_question_id": 771,
  "media_question_name": "1",
  "media_question_main_paragraph": "<Image>",
  "question_list": [
    {
      "question_id": 1216,
      "question_number": 1,
      "question_content": "",
      "answer_list": [
        { "answer_id": 4781, "content": "A", "is_correct": true },
        { "answer_id": 4782, "content": "B", "is_correct": false },
        { "answer_id": 4783, "content": "C", "is_correct": false },
        { "answer_id": 4784, "content": "D", "is_correct": false }
      ]
    }
  ]
}
```

**Note:** The image represents the stimulus; question content is empty because the question refers to the displayed image.

#### Scenario 2: Multi-Question Media (Parts 3/4/6/7)

When a media group contains a passage or listening stimulus, it can have multiple questions. Below is a real example (questions 153–155):

```json
{
  "media_question_id": 1039,
  "media_question_name": "153-155",
  "media_question_main_paragraph": "<Image or Passages>",
  "question_list": [
    {
      "question_id": 1626,
      "question_number": 153,
      "question_content": "Which of the following is NOT a condition placed on receiving the discount?",
      "answer_list": [
        { "answer_id": 6421, "content": "A. A guest must use a specific type of credit card to pay for a room.", "is_correct": false },
        { "answer_id": 6422, "content": "B. The booking must be done well in advance of checking into the hotel.", "is_correct": false },
        { "answer_id": 6423, "content": "C. The reservations must be carried out by calling the toll-free number.", "is_correct": false },
        { "answer_id": 6424, "content": "D. Guests must make their payments in cash.", "is_correct": true }
      ]
    },
    {
      "question_id": 1627,
      "question_number": 154,
      "question_content": "What will the discount apply to?",
      "answer_list": [
        { "answer_id": 6425, "content": "A. Accommodations", "is_correct": true },
        { "answer_id": 6426, "content": "B. Meals", "is_correct": false },
        { "answer_id": 6427, "content": "C. Transportation", "is_correct": false },
        { "answer_id": 6428, "content": "D. Sales tax", "is_correct": false }
      ]
    },
    {
      "question_id": 1628,
      "question_number": 155,
      "question_content": "What can be implied from the advertisement?",
      "answer_list": [
        { "answer_id": 6429, "content": "A. Most travelers don't make a habit of making reservations prior to checking in.", "is_correct": false },
        { "answer_id": 6430, "content": "B. There is a business relationship between the credit card company and the hotel.", "is_correct": true },
        { "answer_id": 6431, "content": "C. The hotel gets very busy during the summer season.", "is_correct": false },
        { "answer_id": 6432, "content": "D. It usually takes a minimum of 10 days for a credit card to clear.", "is_correct": false }
      ]
    }
  ]
}
```

#### Scenario 3: Part 6 (Passage + 4 Questions)

```json
{
  "media_question_id": 3005,
  "media_question_name": "131-134",
  "media_question_main_paragraph": "<Image or Passages>",
  "question_list": [
    { "question_id": 2100, "question_number": 131, "question_content": "...", "answer_list": [...] },
    { "question_id": 2101, "question_number": 132, "question_content": "...", "answer_list": [...] },
    { "question_id": 2102, "question_number": 133, "question_content": "...", "answer_list": [...] },
    { "question_id": 2103, "question_number": 134, "question_content": "...", "answer_list": [...] }
  ]
}
```

#### Scenario 4: Part 7 (Single or Multiple Passages)

Part 7 media groups may contain single or multiple passages. Each media group bundles the questions referencing the same passage(s).

```json
{
  "media_question_id": 4002,
  "media_question_name": "176-178",
  "media_question_main_paragraph": "<Image or Passages>",
  "question_list": [
    { "question_id": 2500, "question_number": 176, "question_content": "...", "answer_list": [...] },
    { "question_id": 2501, "question_number": 177, "question_content": "...", "answer_list": [...] },
    { "question_id": 2502, "question_number": 178, "question_content": "...", "answer_list": [...] }
  ]
}
```

---

## 4. toeicapp_testpart

**Purpose:** Link tests to their corresponding parts (many-to-many relationship).

| Field   | Type   | Null | Key | Default | Extra          |
| ------- | ------ | ---- | --- | ------- | -------------- |
| id      | bigint | NO   | PRI |         | auto_increment |
| part_id | bigint | NO   | MUL |         |                |
| test_id | bigint | NO   | MUL |         |                |

---

## 5. toeicapp_part

**Purpose:** Store TOEIC part data and audio URLs.

| Field      | Type         | Null | Key | Default | Extra          |
| ---------- | ------------ | ---- | --- | ------- | -------------- |
| id         | bigint       | NO   | PRI |         | auto_increment |
| part_order | varchar(255) | NO   |     |         |                |
| title      | longtext     | YES  |     |         |                |
| audio_url  | longtext     | YES  |     |         |                |

---

## 6. toeicapp_question

**Purpose:** Store TOEIC question data and AI-generated translations and explanations.

**Special Columns**

These columns store translation and explanation data generated by AI:

- **`question_translate_json`:** Stores the translated question in JSON format.
  ```json
  {
    "question_id": <int>,
    "question_content": "<translated question>",
    "answer_list": ["<translated answer 1>", "<translated answer 2>", ...],
    "language_id": <language_id>
  }
  ```

- **`question_explain_json`:** Stores detailed explanations in JSON format.
  ```json
  {
    "language_id": <language_id>,
    "question_id": <question_id>,
    "question_need": "<explanation of what the question requires>",
    "question_ask": "<explanation of what the question asks>",
    "correct_answer_reason": "<explanation of why the correct answer is correct>",
    "incorrect_answer_reason": {
      "<answer_label>": "<explanation of why this option is incorrect>",
      ...
    }
  }
  ```


| Field                   | Type         | Null | Key | Default | Extra          |
| ----------------------- | ------------ | ---- | --- | ------- | -------------- |
| id                      | bigint       | NO   | PRI |         | auto_increment |
| content                 | longtext     | YES  |     |         |                |
| question_number         | int unsigned | NO   |     |         |                |
| media_group_id          | bigint       | NO   | MUL |         |                |
| part_id                 | bigint       | NO   | MUL |         |                |
| question_explain_json   | json         | YES  |     |         |                |
| question_translate_json | json         | YES  |     |         |                |

---

## 7. toeicapp_answer

**Purpose:** Store answer choices for TOEIC questions. 
| Field       | Type         | Null | Key | Default | Extra          |
| ----------- | ------------ | ---- | --- | ------- | -------------- |
| id          | bigint       | NO   | PRI |         | auto_increment |
| content     | varchar(255) | NO   |     |         |                |
| is_correct  | tinyint(1)   | NO   |     |         |                |
| question_id | bigint       | NO   | MUL |         |                |

---

## 8. toeicapp_history

**Purpose:** Store user test attempt history and progress data.

**Special Columns**

- **`practice_duration`:** Time duration in Practice mode (integer, counts up from 0)
- **`exam_duration`:** Time duration in Exam mode (integer, counts down from the test's `duration`)
- **`type`:** Test mode type: `"Practice"` or `"Exam"`
- **`dataprogress`:** User answers stored as JSON in the format `{question_id: answer_id}`
- **`part`:** Selected part IDs stored as JSON array.
  - In Practice mode: Contains selected part IDs (users can choose specific parts)
  - In Exam mode: Empty array `[]` (all parts are included)
   
| Field             | Type        | Null | Key | Default           | Extra             |
| ----------------- | ----------- | ---- | --- | ----------------- | ----------------- |
| id                | bigint      | NO   | PRI |                   | auto_increment    |
| dataprogress      | json        | NO   |     |                   |                   |
| type              | varchar(20) | NO   |     |                   |                   |
| part              | json        | YES  |     |                   |                   |
| practice_duration | int         | YES  |     |                   |                   |
| test_id           | bigint      | NO   | MUL |                   |                   |
| user_id           | bigint      | NO   | MUL |                   |                   |
| create_at         | datetime    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| status            | varchar(10) | NO   |     |                   |                   |
| exam_duration     | int         | YES  |     |                   |                   |

---

## 10. Unused Tables

The following tables are currently unused and should be ignored:

- `toeicapp_language`
- `toeicapp_testbank`