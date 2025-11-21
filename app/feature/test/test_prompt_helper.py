from ...util.languge_util import getLanguageById


def build_question_translation_prompt(question_block_json, language_id: str):
    """
    Build a translation prompt for a single question block.

    INPUTS
    -------
    question_block_json: 
        {
            "question_id": <int>,                  # Unique question ID
            "question_content": <str>,             # Question text
            "answer_list": [<str>, <str>, ...]    # List of answer options
        }

    language_id : str  

    OUTPUT
    -------
    The expected **translated JSON** (returned by the LLM after using this prompt)  
    MUST have the exact same structure as the input, with all string values translated  
    and an additional field `"language_id"` appended at the top level.

    Structure (mandatory):
    {
        "question_id": <int>,
        "question_content": <translated str>,
        "answer_list": [<translated str>, <translated str>, ...],
        "language_id": <same language_id as input>
    }

    NOTE:
        - This function itself only builds and returns the prompt string.
        - The LLM must respond with a single valid JSON object matching the schema above.
        - No extra fields, comments, or text are allowed.
    """
    
    target_language = getLanguageById(language_id)

    prompt = f"""
    You are a JSON translator.
    Given a JSON object, translate all string values into {target_language} while keeping the JSON structure, keys, and formatting exactly the same.
    Do not add or remove anything from the original object's structure.
    After translating, add a new field named "language_id" with the value of "{language_id}" to the top level of the JSON object.
    
    CRITICAL: Your response must be ONLY a raw JSON object. 
    - DO NOT wrap it in markdown code blocks (no ```json or ```)
    - DO NOT add any explanatory text before or after the JSON
    - Start your response with {{ and end with }}
    - No comments, no explanations, just pure JSON

    Input: {question_block_json}
    """
    return prompt


def build_question_explain_prompt(question_explain_block_json, language_id):
    target_language = getLanguageById(language_id)
    
    prompt = f"""
    You are an educational reasoning generator.
    You are given a JSON input with the following structure:
    {{
    "question_id": <number>,
    "question_content": "<string>",
    "answer_list": [
        {{ "is_correct": <0 or 1>, "answer_content": "<string>" }},
        ...
    ],
    "language_id": <number>
    }}

    YOUR TASKS:
    Given the JSON input below, analyze the question (“question_content”) and provide concise explanations for:
    - What the question is asking for.
    - What the question means or focuses on.
    - Why the correct answer(s) is/are correct.
    - Why the incorrect answer(s) are wrong.

    Then, translate all explanations into {target_language}.

    After all the tasks, add a new field named "language_id" with the value of "{language_id}" to the top level of the JSON object.
    Return the result in the following JSON format:

    {{
    "language_id": <same language_id>,
    "question_id": <same question_id>,
    "question_need": "<translated explanation of what the question needs>",
    "question_ask": "<translated explanation of what the question asks>",
    "correct_answer_reason": "<translated explanation why the correct answer is correct>",
    "incorrect_answer_reason": {{
        "<answer_label>": "<translated reason why this option is incorrect>",
        ...
    }}
    }}

    CRITICAL REQUIREMENTS:
    - **STRICTLY AND ONLY return a single, valid, raw JSON object.**
    - **DO NOT wrap in markdown code blocks (no ```json or ```)**
    - **DO NOT include any explanatory text before or after the JSON**
    - **Start your response with {{ and end with }}**
    - Keep the original answer labels exactly as they appear in the input (e.g., "A. John Trizz.").
    - Do not mention missing data or make meta observations.
    - Your entire response should be parseable by JSON.parse()

    Input: {question_explain_block_json}
    """
    return prompt


def clean_gemini_response(gemini_resp: str) -> str:
    """
    Clean Gemini API response by removing markdown code block formatting.
    
    Args:
        gemini_resp: Raw response string from Gemini API
        
    Returns:
        Cleaned response string with markdown formatting removed
        
    Example:
        Input: "```json\n{\"key\": \"value\"}\n```"
        Output: "{\"key\": \"value\"}"
    """
    cleaned_resp = gemini_resp.strip()
    
    if cleaned_resp.startswith('```'):
        # Remove markdown code block formatting
        lines = cleaned_resp.split('\n')
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line (```)
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        cleaned_resp = '\n'.join(lines).strip()
    
    return cleaned_resp
