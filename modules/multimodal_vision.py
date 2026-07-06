import re
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_profile_image(uploaded_file):
    """Processes an actual uploaded Streamlit file object using real OCR."""
    try:
        if uploaded_file is None:
            return {"raw_ocr_dump": "", "embedded_phones": [], "embedded_emails": []}
            
        # Open the actual uploaded file stream directly
        img = Image.open(uploaded_file)
        gray_img = img.convert('L') # Optimize contrast
        
        # Run real character recognition
        extracted_raw_text = pytesseract.image_to_string(gray_img)
        
        # Parse real intelligence artifacts out of the text
        phone_matches = re.findall(r'\+?\d{10,12}', extracted_raw_text)
        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', extracted_raw_text)
        
        return {
            "raw_ocr_dump": extracted_raw_text.strip(),
            "embedded_phones": phone_matches,
            "embedded_emails": email_matches
        }
    except Exception as e:
        return {
            "raw_ocr_dump": f"OCR Engine Error: {str(e)}",
            "embedded_phones": [],
            "embedded_emails": []
        }