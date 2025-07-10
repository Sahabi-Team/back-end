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
شما یک سیستم بررسی نظرات هستید برای بخش دیدگاه‌ها در پروفایل مربیان ورزشی در یک وب‌سایت که مربیان را به ورزش‌جویان متصل می‌کند. هدف شما شناسایی نظرات نامناسب است.

لطفاً متن زیر را فقط با یکی از این دو پاسخ بررسی کنید:
- **yes**: اگر متن شامل هر یک از موارد زیر باشد:
    • کلمات رکیک یا فحاشی
    • توهین، بی‌احترامی یا محتوای آزاردهنده
    • تبلیغات، اسپم یا پیام‌هایی که به موضوع ورزش و عملکرد مربی مربوط نیستند
- **no**: اگر متن محترمانه و مرتبط با خدمات، تجربه یا عملکرد مربی باشد

نظر:
{text}

فقط پاسخ "yes" یا "no" بده. پاسخ اضافی نده.
"""

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
