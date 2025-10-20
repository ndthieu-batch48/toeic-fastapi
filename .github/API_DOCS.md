# API DOCUMENTATION

Base url: <YOUR_HOST>/fastapi/
For example: http://localhost:8000/fastapi/

## Endpoints

### I. Test features

`GET /tests`

- Returns a list of all TOEIC test summaries.

##### Response Schema

```json
[  
  {  
    "test_id": 0,
    "test_title": "string",
    "test_duration": 0,
    "test_descrip": "string",
    "part_list": [
      {
        "part_id": 0,
        "part_order": "string",
        "part_title": "string",
        "total_ques": 0
      }
    ]
  }
]
```

##### Store Procedures Used

- `SELECT_ALL_TEST_PROC`

---


`GET /tests/{id}`

- Returns detailed information for a specific TOEIC test, including selected parts and questions.
- **Query Parameters:**
  - `part_ids` (optional, array of int): List of part IDs to filter by. Example: `/tests/1?part_ids=1&part_ids=2`

##### Response Schema

```json
{
  "part_list": [
    {
      "part_id": 0,
      "part_order": "string",
      "part_title": "string",
      "part_audio_url": "string",
      "media_ques_list": [
        {
          "media_ques_id": 0,
          "media_ques_name": "string",
          "media_ques_main_parag": "string",
          "media_ques_audio_script": "string",
          "media_ques_explain": "string",
          "media_ques_trans_script": "string",
          "ques_list": [
            {
              "ques_id": 0,
              "ques_number": 0,
              "ques_content": "string",
              "ans_list": [
                {
                  "ans_id": 0,
                  "content": "string",
                  "is_correct": true
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

##### Store Procedures Used
- `SELECT_TEST_DETAIL_PROC`

---

`POST /tests/gemini/trans/ques`

- Translates a TOEIC question to the target language using Gemini AI.

##### Response Schema

```json
{
  "ques_id": 0,
  "ques_content": "string",
  "ans_list": [
    "string"
  ],
  "lang_id": "vi"
}
```

##### Queries Used
- `SELECT_QUES_BLOCK_JSON_BY_ID`

---

`GET /tests/{test_id}/part/{part_id}/audio/url`

- Returns the stream URL for audio. Returns null for Parts 5, 6, 7.

##### Response Schema

```json
{
  "audio_stream_url": "string | null"
}
```

##### Queries Used
- `SELECT_PART_AUDIO_URL`

---

`GET /tests/{test_id}/part/{part_id}/audio/stream`

- Streams the audio file for a test part.

##### Response Schema
- Returns audio file (MPEG format)

##### Queries Used
- `SELECT_PART_AUDIO_URL`





