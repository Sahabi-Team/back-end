import os
import logging
import openai
from dotenv import load_dotenv

load_dotenv()

import os
import logging
import openai

class PersianSwearWordRemover:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY") 
        openai.api_base = os.getenv("OPENAI_API_BASE") 
        self.model = os.getenv("OPENAI_MODEL_NAME")

    def contains_swear_word(self, text):
        prompt = f"""

لطفاً متن زیر را فقط با یکی از این دو پاسخ بررسی کنید:
- **yes**: اگر متن دارای فحش یا ناسزا باشد
- **no**: اگر متن محترمانه  باشد

نظر:
{text}

فقط پاسخ "yes" یا "no" بده. پاسخ اضافی نده.
"""
        print(os.getenv("OPENAI_API_KEY") )
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=3
            )
            # print("dbg>> ",text,response)
            result = response.choices[0].message.content.strip().lower()
            return result == "yes", result
        except Exception as e:
            logging.error(f"Chat API error: {e}")
            return False, "error"
