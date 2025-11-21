# Document: https://ai.google.dev/gemini-api/docs/quickstart?lang=python
# Migration from googol-genativeai to gemini-api: https://ai.google.dev/gemini-api/docs/migrate
from typing import Optional
from google import genai
from google.genai import types
from .app_config import app_config

# import os, ssl, certifi

# custom_ca = "C:/cert/tma.com.vn/tma.com.vn-full.crt"

# # Create a new PEM bundle at runtime (not stored permanently)
# ctx = ssl.create_default_context(cafile=certifi.where())
# ctx.load_verify_locations(cafile=custom_ca)

# # Save the combined context into a temp file so google-genai can see it
# import tempfile
# with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as tmp:
#     # Dump certifi + your CA into one file
#     with open(certifi.where(), "rb") as f:
#         tmp.write(f.read())
#     with open(custom_ca, "rb") as f:
#         tmp.write(f.read())
#     tmp_path = tmp.name

# # Point google-genai to that temporary file
# os.environ["SSL_CERT_FILE"] = tmp_path

gemini_client = genai.Client(api_key=app_config.GEMINI_API_KEY)

def generate_text_with_gemini(prompt: str):
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        error_message = f"Gemini API error: {type(e).__name__} - {str(e)}"
        print(error_message)  # Log the error
        
        # Check if it's a 5xx server error (503, 500, etc.)
        error_str = str(e)
        if '503' in error_str or '500' in error_str or '502' in error_str or 'overloaded' in error_str.lower():
            # Try gemini-2.0-flash first
            print("Attempting fallback to gemini-2.0-flash due to server error...")
            try:
                response = gemini_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                print("Successfully used fallback model gemini-2.0-flash")
                return response.text
            except Exception as fallback_error_2_0:
                print(f"gemini-2.0-flash failed: {str(fallback_error_2_0)}")
                
                # Try gemini-1.5-flash as final fallback
                print("Attempting final fallback to gemini-1.5-flash...")
                try:
                    response = gemini_client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    print("Successfully used fallback model gemini-1.5-flash")
                    return response.text
                except Exception as fallback_error_1_5:
                    fallback_message = f"All fallback models failed. Last error: {type(fallback_error_1_5).__name__} - {str(fallback_error_1_5)}"
                    print(fallback_message)
                    raise Exception(fallback_message) from fallback_error_1_5
        
        raise Exception(error_message) from e
