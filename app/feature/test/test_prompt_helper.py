from ...util.languge_util import getLangById


def build_ques_trans_prompt(ques_block_json, lang_id):
    """
    Build a translation prompt for a single question block.

    INPUTS
    -------
    ques_block_json : dict  
        Source: returned from the SQL query `SELECT_QUES_BLOCK_JSON_BY_ID`.
        Structure (mandatory):
        {
            "ques_id": <int>,                  # Unique question ID
            "ques_content": <str>,             # Question text
            "ans_list": [<str>, <str>, ...]    # List of answer options
        }

    lang_id : int | str  
        Source: returned from the `getLangById()` function.
        Represents the target language identifier (used to determine the translation language).

    OUTPUT
    -------
    The expected **translated JSON** (returned by the LLM after using this prompt)  
    MUST have the exact same structure as the input, with all string values translated  
    and an additional field `"lang_id"` appended at the top level.

    Structure (mandatory):
    {
        "ques_id": <int>,
        "ques_content": <translated str>,
        "ans_list": [<translated str>, <translated str>, ...],
        "lang_id": <same lang_id as input>
    }

    NOTE:
        - This function itself only builds and returns the prompt string.
        - The LLM must respond with a single valid JSON object matching the schema above.
        - No extra fields, comments, or text are allowed.
    """
    
    target_lang = getLangById(lang_id)

    prompt = f"""
    You are a JSON translator.
    Given a JSON object, translate all string values into {target_lang} while keeping the JSON structure, keys, and formatting exactly the same.
    Do not add or remove anything from the original object's structure.
    After translating, add a new field named "lang_id" with the value of "{lang_id}" to the top level of the JSON object.
    Your response must be a single, valid JSON object, with no comments, explanations, or code block formatting (e.g., no backticks or language specifiers).

    Input: {ques_block_json}
    """
    return prompt


def build_ques_explain_prompt(ques_explain_block_json, lang_id):
    target_lang = getLangById(lang_id)
    
    prompt = f"""
    You are an educational reasoning generator.
    You are given a JSON input with the following structure:
    {{
    "ques_id": <number>,
    "ques_content": "<string>",
    "ans_list": [
        {{ "is_correct": <0 or 1>, "ans_content": "<string>" }},
        ...
    ],
    "lang_id": <number>
    }}

    YOUR TASKS:
    Given the JSON input below, analyze the question (“ques_content”) and provide concise explanations for:
    - What the question is asking for.
    - What the question means or focuses on.
    - Why the correct answer(s) is/are correct.
    - Why the incorrect answer(s) are wrong.

    Then, translate all explanations into {target_lang}.

    After all the tasks, add a new field named "lang_id" with the value of "{lang_id}" to the top level of the JSON object.
    Return the result in the following JSON format:

    {{
    "lang_id": <same lang_id>,
    "ques_id": <same ques_id>,
    "ques_need": "<translated explanation of what the question needs>",
    "ques_ask": "<translated explanation of what the question asks>",
    "correct_ans_reason": "<translated explanation why the correct answer is correct>",
    "incorrect_ans_reason": {{
        "<answer_label>": "<translated reason why this option is incorrect>",
        ...
    }}
    }}

    Additional requirements:
    - **STRICTLY AND ONLY return a single, valid, raw JSON object.**
    - **DO NOT include any Markdown formatting, code blocks (e.g., ```json or ```), comments, or surrounding text outside of the JSON object.**
    - Keep the original answer labels exactly as they appear in the input (e.g., "A. John Trizz.").
    - Do not mention missing data or make meta observations.
    - The response must start with '{{' and end with '}}'.

    Input: {ques_explain_block_json}
    """
    return prompt
