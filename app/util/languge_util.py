from typing import Literal


LANGUAGE_MAP = {
    "vi": "Vietnamese",
    "ja": "Japanese", 
    "en": "English",
}


LanguageCode = Literal["vi", "ja", "en"]


def getLanguageById(langId):
    """
    Get language name by language ID or code.
    
    Args:
        langId: Language code (str)
        
    Returns:
        str: Language name, defaults to Vietnamese if not found
    """
    return LANGUAGE_MAP.get(langId, "Vietnamese")