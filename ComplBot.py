import logging
import random
import asyncio
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

BOT_TOKEN = '7107502057:AAFuiE61PplT_EXScOY6L9SyjtteGYZASns'

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Локализация
TEXTS = {
    "ru": {
        "main_menu": "🌟 <b>Главное меню</b> 🌟\n\nВыберите действие:",
        "compliment_btn": "💖 Сгенерировать комплимент",
        "fact_btn": "🧠 Случайный факт",
        "rate_btn": "⭐ Оценить бота",
        "help_btn": "ℹ️ Помощь",
        "compliment_title": "💖 <b>Ваш комплимент:</b>",
        "fact_title": "🧠 <b>Интересный факт:</b>",
        "rate_title": "⭐ <b>Оцените бота:</b>",
        "thanks_rating": "🙏 <b>Спасибо за {stars} оценку!</b>",
        "help_text": (
            "ℹ️ <b>Помощь</b>\n\n"
            "Этот бот создан, чтобы поднимать настроение!\n\n"
            "• Нажмите <b>Сгенерировать комплимент</b> для получения случайного комплимента\n"
            "• Выберите <b>Случайный факт</b> для интересной информации\n"
            "• Оцените бота, если вам понравилось!"
            "• Бот защищен Apache License: https://www.apache.org/licenses/LICENSE-2.0"
            "• Создатель бота @Girlanda228"
        ),
        "back_btn": "🔙 Назад",
        "choose_language": "🌍 <b>Выберите язык:</b>",
        "language_select": "🇷🇺 Русский"
    },
    "en": {
        "main_menu": "🌟 <b>Main Menu</b> 🌟\n\nChoose an action:",
        "compliment_btn": "💖 Generate compliment",
        "fact_btn": "🧠 Random fact",
        "rate_btn": "⭐ Rate bot",
        "help_btn": "ℹ️ Help",
        "compliment_title": "💖 <b>Your compliment:</b>",
        "fact_title": "🧠 <b>Interesting fact:</b>",
        "rate_title": "⭐ <b>Rate the bot:</b>",
        "thanks_rating": "🙏 <b>Thank you for {stars} rating!</b>",
        "help_text": (
            "ℹ️ <b>Help</b>\n\n"
            "This bot was created to cheer you up!\n\n"
            "• Click <b>Generate compliment</b> to get a random compliment\n"
            "• Select <b>Random fact</b> for interesting information\n"
            "• Rate the bot if you liked it!"
            "• Bot protected by Apache License: https://www.apache.org/licenses/LICENSE-2.0"
            "• Bot creator @Girlanda228"
        ),
        "back_btn": "🔙 Back",
        "choose_language": "🌍 <b>Choose language:</b>",
        "language_select": "🇬🇧 English"
    }
}

# Списки сообщений
COMPLIMENTS = {
    "ru": [
        "Вы — настоящее солнце в пасмурный день! ☀️",
        "Ваш стиль неподражаем! 👗✨",
        "У вас самая добрая душа! 💖",
        "Вы умны, как энциклопедия, и обаятельны, как весенний день! 📚🌷",
        "С вами время летит незаметно! ⏳💫",
        "Ваша харизма покоряет всех вокруг! 🔥",
        "Вы умеете слушать, и это бесценно! 👂💎",
        "Ваш смех — лучший звук на свете! 😄🎶",
        "Вы вдохновляете людей просто быть рядом! 🌟",
        "Ваша уверенность восхищает! 💪👑",
        "Вы преображаете любое пространство вокруг себя! 🎨",
        "С вами хочется становиться лучше! 🌱",
        "Ваша искренность — ваша суперсила! 💫",
        "Вы умеете находить красоту в мелочах! 🌸",
        "Ваша мудрость впечатляет! 🦉",
        "Вы — человек, с которым хочется делиться секретами! 🤫💞",
        "Ваше чувство юмора — на миллион! 😂💰",
        "Вы умеете делать обычные моменты волшебными! ✨",
        "Ваша доброта согревает сердца! 🔥💛",
        "Вы — воплощение элегантности! 🎩🌹"
    ],
    "en": [
        "You light up the room! ✨",
        "Your smile is contagious! 😊",
        "You're an incredible friend! 👫",
        "You're smarter than Google and more fun than TikTok! 📱😂",
        "Time spent with you is time well spent! ⏳💎",
        "You have the best laugh! 😄🎵",
        "You're like sunshine on a rainy day! ☀️",
        "Your positive attitude is inspiring! 🌟",
        "You're someone everyone looks up to! 👆✨",
        "You have a heart of gold! 💛",
        "Your creativity knows no bounds! 🎨",
        "You make the world a better place! 🌍💖",
        "You're a true original! 🦄",
        "You're cooler than the other side of the pillow! ❄️",
        "You're the human equivalent of a cozy blanket! 🧶",
        "You're more fun than a basket of puppies! 🐶",
        "You're the MVP of life! 🏆",
        "You're the person everyone hopes to meet! 🤩",
        "You're making a difference just by being you! 💪",
        "You're the definition of awesome! 🤘"
    ]
}

FACTS = {
    "ru": [
        "🦈 Акулы существуют дольше, чем деревья! (400 млн лет)",
        "🍯 Мёд никогда не портится – археологи находили съедобный мёд возрастом 3000 лет!",
        "🐧 Пингвины могут прыгать до 2 метров в высоту!",
        "🌙 На Луне есть запах... жареного мяса (по словам астронавтов)!",
        "🦷 Зубная эмаль — самая твердая ткань в организме!",
        "🐌 У улиток около 25 000 зубов!",
        "🕷️ Пауки могут ходить по воде благодаря поверхностному натяжению!",
        "🍌 Бананы — это ягоды, а клубника — нет!",
        "🦒 У жирафов и людей одинаковое количество шейных позвонков — 7!",
        "☕ Кофеин начинает действовать уже через 10 минут после употребления!",
        "🦴 Ребенок рождается с 270 костями, а у взрослого их всего 206!",
        "🐝 Пчелы общаются с помощью танца!",
        "🌊 Океаны содержат 99% жизненного пространства на Земле!",
        "🦇 Летучие мыши — единственные млекопитающие, способные к полету!",
        "📱 Смартфоны мощнее компьютеров, использовавшихся для полета на Луну!",
        "🦜 Попугаи могут жить дольше людей (некоторые виды — до 80 лет)!",
        "🍎 Яблоки плавают, потому что на 25% состоят из воздуха!",
        "🚀 Венера — единственная планета, вращающаяся против часовой стрелки!",
        "🦓 Зебры белые с черными полосками, а не наоборот!",
        "🧬 ДНК человека на 50% совпадает с ДНК банана!"
    ],
    "en": [
        "🦈 Sharks existed before trees! (400 million years)",
        "🍯 Honey never spoils - archaeologists found edible honey from 3000 years ago!",
        "🐧 Penguins can jump up to 6 feet high!",
        "🌙 The Moon smells like gunpowder (according to astronauts)!",
        "🦷 Tooth enamel is the hardest substance in the human body!",
        "🐌 Snails have about 25,000 teeth!",
        "🕷️ Some spiders can 'sail' across water using their legs as sails!",
        "🍌 Bananas are berries, but strawberries aren't!",
        "🦒 Giraffes and humans have the same number of neck vertebrae (7)!",
        "☕ Caffeine starts working within 10 minutes of consumption!",
        "🦴 Babies are born with 270 bones, adults have only 206!",
        "🐝 Honeybees communicate through 'waggle dances'!",
        "🌊 The ocean contains 99% of Earth's living space!",
        "🦇 Bats are the only mammals capable of sustained flight!",
        "📱 Your smartphone is millions of times more powerful than Apollo 11's computers!",
        "🦜 Some parrots can live over 80 years!",
        "🍎 Apples float because they're 25% air!",
        "🚀 Venus is the only planet that rotates clockwise!",
        "🦓 Zebras are white with black stripes, not black with white stripes!",
        "🧬 Humans share 50% of their DNA with bananas!"
    ]
}

# Разные изображения для каждого языка
MENU_PHOTOS = {
    "ru": "https://postimg.cc/9RgKg9bM",  # Замените на свою русскую версию
    "en": "https://postimg.cc/yDh54tj2"    # Замените на свою английскую версию
}

# Изображение для выбора языка
LANGUAGE_PHOTO = "https://postimg.cc/BXH7Hkrt"  # Замените на свое изображение

async def send_main_menu(chat_id, context, edit_message_id=None, lang="ru"):
    """Отправка/обновление главного меню с картинкой на выбранном языке"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(TEXTS[lang]["compliment_btn"], callback_data=f"compliment_{lang}")],
        [InlineKeyboardButton(TEXTS[lang]["fact_btn"], callback_data=f"fact_{lang}")],
        [InlineKeyboardButton(TEXTS[lang]["rate_btn"], callback_data=f"rate_{lang}")],
        [InlineKeyboardButton(TEXTS[lang]["help_btn"], callback_data=f"help_{lang}")],
        [InlineKeyboardButton(TEXTS[lang]["language_select"], callback_data="change_language")]
    ])
    
    photo_url = MENU_PHOTOS[lang]
    
    if edit_message_id:
        await context.bot.edit_message_media(
            chat_id=chat_id,
            message_id=edit_message_id,
            media=InputMediaPhoto(media=photo_url, caption=TEXTS[lang]["main_menu"], parse_mode='HTML'),
            reply_markup=keyboard
        )
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=TEXTS[lang]["main_menu"],
            parse_mode='HTML',
            reply_markup=keyboard
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start с выбором языка"""
    user = update.effective_user
    logger.info(f"User {user.id} started the bot")
    
    # Клавиатура выбора языка
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")]
    ])
    
    await update.message.reply_photo(
        photo=LANGUAGE_PHOTO,
        caption=TEXTS["ru"]["choose_language"],
        parse_mode='HTML',
        reply_markup=keyboard
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий inline-кнопок"""
    query = update.callback_query
    await query.answer()
    
    # Обработка смены языка
    if query.data == "change_language":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")]
        ])
        
        current_lang = context.user_data.get("lang", "ru")
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=LANGUAGE_PHOTO,
                caption=TEXTS[current_lang]["choose_language"],
                parse_mode='HTML'
            ),
            reply_markup=keyboard
        )
        return
    
    # Обработка выбора языка
    if query.data.startswith("set_lang_"):
        lang = query.data.split("_")[-1]
        context.user_data["lang"] = lang
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)
        return
    
    # Разделяем callback_data на действие и язык
    if "_" in query.data:
        action, lang = query.data.split("_", 1)
    else:
        action = query.data
        lang = context.user_data.get("lang", "ru")
    
    if action == "compliment":
        compliment = random.choice(COMPLIMENTS[lang])
        if query.message.photo:
            await query.edit_message_caption(
                caption=f"{TEXTS[lang]['compliment_title']}\n\n{compliment}",
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                f"{TEXTS[lang]['compliment_title']}\n\n{compliment}",
                parse_mode='HTML'
            )
        await asyncio.sleep(3)
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)
        
    elif action == "fact":
        fact = random.choice(FACTS[lang])
        if query.message.photo:
            await query.edit_message_caption(
                caption=f"{TEXTS[lang]['fact_title']}\n\n{fact}",
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                f"{TEXTS[lang]['fact_title']}\n\n{fact}",
                parse_mode='HTML'
            )
        await asyncio.sleep(3)
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)
        
    elif action == "rate":
        await show_rating_menu(query, context, lang)
        
    elif action == "help":
        if query.message.photo:
            await query.edit_message_caption(
                caption=TEXTS[lang]["help_text"],
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                TEXTS[lang]["help_text"],
                parse_mode='HTML'
            )
        await asyncio.sleep(5)
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)

async def show_rating_menu(query, context, lang="ru"):
    """Показать меню оценки"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐", callback_data=f"rate1_{lang}"),
         InlineKeyboardButton("⭐⭐", callback_data=f"rate2_{lang}"),
         InlineKeyboardButton("⭐⭐⭐", callback_data=f"rate3_{lang}")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data=f"rate4_{lang}"),
         InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data=f"rate5_{lang}")],
        [InlineKeyboardButton(TEXTS[lang]["back_btn"], callback_data=f"back_{lang}")]
    ])
    
    if query.message.photo:
        await query.edit_message_caption(
            caption=TEXTS[lang]["rate_title"],
            parse_mode='HTML',
            reply_markup=keyboard
        )
    else:
        await query.edit_message_text(
            TEXTS[lang]["rate_title"],
            parse_mode='HTML',
            reply_markup=keyboard
        )

async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка оценки"""
    query = update.callback_query
    await query.answer()
    
    # Получаем язык и оценку
    if "_" in query.data:
        rating_part, lang = query.data.rsplit("_", 1)
    else:
        rating_part = query.data
        lang = context.user_data.get("lang", "ru")
    
    if rating_part.startswith("rate"):
        stars = int(rating_part.replace("rate", ""))
        star_icons = "⭐" * stars
        if query.message.photo:
            await query.edit_message_caption(
                caption=TEXTS[lang]["thanks_rating"].format(stars=star_icons),
                parse_mode='HTML'
            )
        else:
            await query.edit_message_text(
                TEXTS[lang]["thanks_rating"].format(stars=star_icons),
                parse_mode='HTML'
            )
        await asyncio.sleep(2)
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)
    elif rating_part == "back":
        await send_main_menu(query.message.chat_id, context, query.message.message_id, lang)

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(set_lang_|compliment_|fact_|rate_|help_|back_|change_language)"))
    application.add_handler(CallbackQueryHandler(handle_rating, pattern="^rate[1-5]_"))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                        lambda u, c: send_main_menu(u.effective_chat.id, c)))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()