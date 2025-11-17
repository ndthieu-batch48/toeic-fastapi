# import os
# import easyocr
# import base64
# import numpy as np
# import cv2
# from typing import Dict
# import io
# from PIL import Image

# MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models', 'easyocr')

# # Initialize EasyOCR reader (load once at startup)
# reader = easyocr.Reader(
#     ['vi', 'ja', 'en'],
#     gpu=False,
#     model_storage_directory=MODEL_DIR
# )

# def base64_to_image(base64_string: str) -> np.ndarray:
#     """Convert base64 string to numpy array (OpenCV format)"""
#     try:
#         # Remove data URL prefix if present
#         if ',' in base64_string:
#             base64_string = base64_string.split(',')[1]
        
#         # Decode base64
#         img_bytes = base64.b64decode(base64_string)
        
#         # Convert to PIL Image then to numpy array
#         img = Image.open(io.BytesIO(img_bytes))
#         img_array = np.array(img)
        
#         # Convert RGB to BGR for OpenCV
#         if len(img_array.shape) == 3 and img_array.shape[2] == 3:
#             img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
#         return img_array
#     except Exception as e:
#         raise ValueError(f"Failed to decode base64 image: {str(e)}")

# def main_paragrap_parser(paragrap_main: str) -> Dict:
#     """
#     Parse text content from base64 image using EasyOCR
    
#     Args:
#         paragrap_main: Base64 encoded image string from database
        
#     Returns:
#         Dict containing:
#             - content: Full text extracted from image
#             - details: List of OCR results with text, confidence, and bounding boxes
            
#     Raises:
#         ValueError: If image decoding fails
#         Exception: If OCR processing fails
#     """
#     try:
#         # Convert base64 to image array
#         img_array = base64_to_image(paragrap_main)
        
#         # Perform OCR using EasyOCR
#         results = reader.readtext(img_array)
        
#         # Format results
#         ocr_details = []
#         all_text = []
        
#         for (bbox, text, prob) in results:
#             ocr_details.append({
#                 "text": text,
#                 "confidence": round(float(prob), 4),
#                 "bbox": [[int(x), int(y)] for x, y in bbox]
#             })
#             all_text.append(text)
        
#         return {
#             "content": " ".join(all_text),
#             "details": ocr_details
#         }
        
#     except ValueError as e:
#         raise ValueError(f"Image decoding error: {str(e)}")
#     except Exception as e:
#         raise Exception(f"OCR processing error: {str(e)}")

