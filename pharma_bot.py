import telebot
from openai import OpenAI
import os
# جلب المتغيرات من البيئة
telegram_token = os.getenv("TELEGRAM_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(telegram_token)
client = OpenAI()

# دالة توليد الجواب من GPT
def generate_answer(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومتخصص لمساعدة طلاب الصيدلة. جاوب بأسلوب تعليمي، واضح، وبسيط."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"حدث خطأ: {e}"

# التعامل مع الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    answer = generate_answer(user_input)

    # إذا الجواب فارغ أو غير واضح
    if not answer or answer.strip() == "":
        answer = "لم أفهم سؤالك تماماً، هل يمكنك توضيحه أكثر؟"

    bot.reply_to(message, answer)

print("✅ البوت يعمل الآن!")
bot.polling()
