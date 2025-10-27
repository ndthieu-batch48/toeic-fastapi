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