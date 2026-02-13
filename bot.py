import telebot
from telebot import types
import openai

# ====== TOKENS ======
TOKEN = "8158930917:AAFhZlS5lKPygn56xRywcgrUueCrbkPMclE"
openai.api_key = "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"



# ====== USER LANGUAGE ======
user_language = {}

# ====== TEXT DATABASE ======
texts = {
    "kz": {
        "menu": "Мәзірді таңдаңыз:",
        "who": "Қорқыт ата — түркі халықтарының ұлы ойшылы, қобыздың атасы.",
        "audio": "🎧 Аудио-гид",
        "photo": "📸 Фотоға ең жақсы орындар:",
        "ask": "🤖 AI-гидке сұрақ қойыңыз"
    },
    "ru": {
        "menu": "Выберите меню:",
        "who": "Коркыт ата — великий мыслитель тюркского мира, основатель кобыза.",
        "audio": "🎧 Аудио-гид",
        "photo": "📸 Лучшие места для фото:",
        "ask": "🤖 Задайте вопрос AI-гиду"
    },
    "en": {
        "menu": "Choose a menu:",
        "who": "Korkyt Ata is a great Turkic thinker and the founder of the kobyz.",
        "audio": "🎧 Audio guide",
        "photo": "📸 Best photo spots:",
        "ask": "🤖 Ask the AI guide"
    },
    "tr": {
        "menu": "Menüden seçiniz:",
        "who": "Korkut Ata, Türk dünyasının büyük düşünürü ve kopuzun kurucusudur.",
        "audio": "🎧 Sesli rehber",
        "photo": "📸 En iyi fotoğraf alanları:",
        "ask": "🤖 AI rehbere soru sor"
    },
    "cn": {
        "menu": "请选择菜单：",
        "who": "科尔库特阿塔是突厥民族伟大的思想家，也是库布兹的创始人。",
        "audio": "🎧 语音导览",
        "photo": "📸 最佳拍照地点：",
        "ask": "🤖 向AI导游提问"
    }
}

# ====== AI SYSTEM PROMPT ======
SYSTEM_PROMPT = """
You are an official tourist guide of the Korkyt Ata Memorial Complex in Kazakhstan.
Answer only questions related to Korkyt Ata, the memorial complex, history, legends, music, and tourism.
If the question is unrelated, politely say that you only provide information about the Korkyt Ata complex.
Use the same language as the user.
Keep answers short, clear, and friendly.
"""

# ====== START & LANGUAGE SELECTION ======
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇰🇿 Қазақша", "🇷🇺 Русский")
    markup.add("🇬🇧 English", "🇹🇷 Türkçe")
    markup.add("🇨🇳 中文")

    bot.send_message(
        message.chat.id,
        "🌍 Тілді таңдаңыз / Choose language",
        reply_markup=markup
    )

# ====== SET LANGUAGE ======
@bot.message_handler(func=lambda m: m.text in [
    "🇰🇿 Қазақша", "🇷🇺 Русский", "🇬🇧 English", "🇹🇷 Türkçe", "🇨🇳 中文"
])
def set_language(message):
    lang_map = {
        "🇰🇿 Қазақша": "kz",
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en",
        "🇹🇷 Türkçe": "tr",
        "🇨🇳 中文": "cn"
    }

    lang = lang_map[message.text]
    user_language[message.chat.id] = lang

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏛 Қорқыт ата кім?")
    markup.add("🎧 Аудио-гид", "📸 Фото-гид")
    markup.add("🤖 AI-гид")

    bot.send_message(
        message.chat.id,
        texts[lang]["menu"],
        reply_markup=markup
    )

# ====== STATIC INFO ======
@bot.message_handler(func=lambda m: m.text == "🏛 Қорқыт ата кім?")
def who_korkyt(message):
    lang = user_language.get(message.chat.id, "kz")
    bot.send_message(message.chat.id, texts[lang]["who"])

# ====== AUDIO GUIDE ======
@bot.message_handler(func=lambda m: m.text == "🎧 Аудио-гид")
def audio(message):
    audio_file = open("audio/korkyt_ata.mp3", "rb")
    lang = user_language.get(message.chat.id, "kz")
    bot.send_audio(
        message.chat.id,
        audio_file,
        caption=texts[lang]["audio"]
    )

# ====== PHOTO GUIDE ======
@bot.message_handler(func=lambda m: m.text == "📸 Фото-гид")
def photo(message):
    lang = user_language.get(message.chat.id, "kz")
    bot.send_message(
        message.chat.id,
        texts[lang]["photo"] + "\n• Күн батар сәт 🌅\n• Мүсін жанында"
    )
    photo1 = open("images/photo1.jpg", "rb")
    bot.send_photo(message.chat.id, photo1)

# ====== AI MODE BUTTON ======
@bot.message_handler(func=lambda m: m.text == "🤖 AI-гид")
def ai_intro(message):
    lang = user_language.get(message.chat.id, "kz")
    bot.send_message(
        message.chat.id,
        texts[lang]["ask"]
    )

# ====== AI ANSWER (MUST BE LAST) ======
@bot.message_handler(func=lambda m: True)
@bot.message_handler(func=lambda m: True)
def ai_answer(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )

        bot.send_message(
            message.chat.id,
            response["choices"][0]["message"]["content"]
        )

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ AI қатесі: " + str(e))


    bot.send_message(
        message.chat.id,
        response.choices[0].message.content
    )

# ====== RUN ======
bot.polling()