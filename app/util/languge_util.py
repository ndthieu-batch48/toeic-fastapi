from typing import Literal


LANG_MAP = {
    "vi": "Vietnamese",
    "ja": "Japanese", 
    "en": "English",
}


LangCode = Literal["vi", "ja", "en"]


def getLangById(langId):
    """
    Get language name by language ID or code.
    
    Args:
        langId: Language code (str)
        
    Returns:
        str: Language name, defaults to Vietnamese if not found
    """
    return LANG_MAP.get(langId, "Vietnamese")