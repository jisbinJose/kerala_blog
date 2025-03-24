from googletrans import Translator
import re

def detect_language(text):
    """
    Detect if text is primarily in English or Malayalam.
    Returns 'en' for English, 'ml' for Malayalam.
    """
    # Simple heuristic: Malayalam characters are in Unicode range 0D00-0D7F
    malayalam_pattern = re.compile(r'[\u0D00-\u0D7F]')
    malayalam_chars = len(malayalam_pattern.findall(text))
    
    # If more than 10% of characters are Malayalam, consider it Malayalam
    if malayalam_chars > len(text) * 0.1:
        return 'ml'
    return 'en'

def translate_text(text, target_language=None):
    """
    Translate text between English and Malayalam.
    If target_language is None, auto-detect and translate to the other language.
    """
    if not text:
        return "", None
        
    translator = Translator()
    
    # Detect source language if target not specified
    if target_language is None:
        source_language = detect_language(text)
        target_language = 'ml' if source_language == 'en' else 'en'
    else:
        source_language = 'ml' if target_language == 'en' else 'en'
    
    try:
        translation = translator.translate(text, src=source_language, dest=target_language)
        return translation.text, target_language
    except Exception as e:
        print(f"Translation error: {e}")
        return text, source_language  # Return original text if translation fails
