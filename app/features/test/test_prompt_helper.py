from ...util.languge_util import getLangById


def build_ques_trans_prompt(ques_block_json, lang_id):
    target_lang = getLangById(lang_id)
    
    prompt = f"""
    You are a JSON translator.
    Given a JSON object, translate all string values into {target_lang} while keeping the JSON structure, keys, and formatting exactly the same.
    Do not add or remove anything from the original object's structure.
    After translating, add a new field named "language_id" with the value of "{lang_id}" to the top level of the JSON object.
    Your response must be a single, valid JSON object, with no comments, explanations, or code block formatting (e.g., no backticks or language specifiers).

    Input: {ques_block_json}
    """
    return prompt