import telebot
from openai import OpenAI
import os
import time
import requests
telegram_token = os.getenv("TELEGRAM_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(telegram_token)
client = client = OpenAI()
def generate_answer(user_input):
    max_retries = 5  # نحاول 5 مرات
    delay = 5  # كل محاولة ننتظر 5 ثواني
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "جاوب بإسلوب واضح وبسيط ومختصر."},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()
            return answer
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
            if attempt < max_retries - 1:
                print(f"فشل الاتصال، المحاولة رقم {attempt + 1}، راح نعيد بعد {delay} ثانية...")
                time.sleep(delay)
                delay *= 2  # نزيد وقت الانتظار بالتدريج
            else:
                return "حدث خطأ في الاتصال. حاول مرة أخرى لاحقاً."
        except Exception as e:
            return f"حدث خطأ آخر: {e}"
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    answer = generate_answer(user_input)
    bot.reply_to(message, answer)
print("البوت يعمل الآن...")
bot.polling()
