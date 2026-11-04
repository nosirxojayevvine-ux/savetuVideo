import os
import threading
from flask import Flask
import telebot
from telebot import types
import yt_dlp

# --- 1. Flask veb-server (Render uchun 24/7 ishchi holat) ---
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot status: Active'


def run_web():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


t = threading.Thread(target=run_web)
t.daemon = True
t.start()

# --- 2. Telegram Bot va Sozlamalar ---
TOKEN = '9228563150:AAHK4E9n5FbprJVRWoqewgp6NOQmPBtoADw'
bot = telebot.TeleBot(TOKEN)

# Sizning Admin ID raqamingiz
ADMIN_ID = 8019481444

# Bot imzosi
ADS_TEXT = '\n\n🤖 **Bot:** @VideoSaveQualityBot'

# --- 3. 4 Tildagi Matnlar Lug'ati ---
TEXTS = {
    'uz': {
        'welcome': (
            '👋 **Salom**\n\n'
            '📥 **Men sizga quyidagi platformalardan video va rasmlarni'
            ' yuklashda yordam beraman:**\n\n'
            '🔴 YouTube\n'
            '📸 Instagram\n'
            '🎵 TikTok\n'
            '📌 Pinterest\n'
            '👻 Snapchat\n'
            '❤️ Likee\n'
            '💙 VK\n'
            '🔵 Facebook\n'
            '🧵 Threads\n'
            '🎵 Music\n\n'
            '• *Videoni yuklash uchun video yoki rasmni havolasini menga'
            " jo'sting*\n\n"
            '(Bot guruhlarda ham ishlaydi, guruhda ham ishlatmoqchi bo\'lsangiz'
            ' tugmani bosing 👇)'
        ),
        'btn_group': "➕ Guruhga qo'shish",
        'lang_changed': "Til O'zbekcha (Lotin) ga o'zgartirildi ✅",
        'downloading': '⏳ Video yuklanmoqda, kuting...',
        'success': 'Yuborgan havolangiz Yuklab olindi📥  @VideoSaveQualityBot nomidan sizga raxmat✊ kelasi linkda kutib qolamiz... !',
    },
    'uz_kr': {
        'welcome': (
            '👋 **Салом**\n\n'
            '📥 **Мен сизга қуйидаги платформалардан видео ва расмларни юклашда'
            ' ёрдам бераман:**\n\n'
            '🔴 YouTube\n'
            '📸 Instagram\n'
            '🎵 TikTok\n'
            '📌 Pinterest\n'
            '👻 Snapchat\n'
            '❤️ Likee\n'
            '💙 VK\n'
            '🔵 Facebook\n'
            '🧵 Threads\n'
            '🎵 Music\n\n'
            '• *Видеони юклаш учун видео ёки расмни ҳаволасини менга'
            " жўртинг*\n\n"
            '(Бот гуруҳларда ҳам ишлайди, гуруҳда ҳам ишлатмоқчи бўлсангиз тугмани'
            ' босинг 👇)'
        ),
        'btn_group': '➕ Гуруҳга қўшиш',
        'lang_changed': 'Тил Ўзбекча (Крил) га ўзгартирилди ✅',
        'downloading': '⏳ Видео юкланмоқда, кутинг...',
        'success': 'Юборган  хаволангиз юуклаб олинди📥 @VideoSaveQualityBot номидан сизга рахмат ва келаси линкда кутиб коламиз.. !',
    },
    'ru': {
        'welcome': (
            '👋 **Привет**\n\n'
            '📥 **Я помогу вам скачать видео и фотографии со следующих'
            ' платформ:**\n\n'
            '🔴 YouTube\n'
            '📸 Instagram\n'
            '🎵 TikTok\n'
            '📌 Pinterest\n'
            '👻 Snapchat\n'
            '❤️ Likee\n'
            '💙 VK\n'
            '🔵 Facebook\n'
            '🧵 Threads\n'
            '🎵 Music\n\n'
            '• *Отправьте мне ссылку на видео или фото для скачивания*\n\n'
            '(Бот также работает в группах, если хотите использовать его в'
            ' группе, нажмите кнопку 👇)'
        ),
        'btn_group': '➕ Добавить в группу',
        'lang_changed': 'Язык изменен на Русский ✅',
        'downloading': '⏳ Загрузка видео, подождите...',
        'success': 'Загружено!',
    },
    'en': {
        'welcome': (
            '👋 **Hello**\n\n'
            '📥 **I can help you download videos and photos from the following'
            ' platforms:**\n\n'
            '🔴 YouTube\n'
            '📸 Instagram\n'
            '🎵 TikTok\n'
            '📌 Pinterest\n'
            '👻 Snapchat\n'
            '❤️ Likee\n'
            '💙 VK\n'
            '🔵 Facebook\n'
            '🧵 Threads\n'
            '🎵 Music\n\n'
            '• *Send me the link of the video or photo to download*\n\n'
            '(The bot also works in groups, if you want to use it in a group,'
            ' click the button 👇)'
        ),
        'btn_group': '➕ Add to group',
        'lang_changed': 'Language changed to English ✅',
        'downloading': '⏳ Downloading video, please wait...',
        'success': 'Downloaded!',
    },
}


# Foydalanuvchi tilini saqlash va o'qish funksiyalari
def set_user_lang(user_id, lang):
  user_id = str(user_id)
  langs = {}
  if os.path.exists('languages.txt'):
    with open('languages.txt', 'r') as f:
      for line in f:
        parts = line.strip().split(':')
        if len(parts) == 2:
          langs[parts[0]] = parts[1]
  langs[user_id] = lang
  with open('languages.txt', 'w') as f:
    for uid, l in langs.items():
      f.write(f'{uid}:{l}\n')


def get_user_lang(user_id):
  user_id = str(user_id)
  if os.path.exists('languages.txt'):
    with open('languages.txt', 'r') as f:
      for line in f:
        parts = line.strip().split(':')
        if len(parts) == 2 and parts[0] == user_id:
          return parts[1]
  return 'uz'  # Standart til - O'zbekcha


# Chatni bazaga saqlash
def save_chat_id(chat_id):
  chat_id = str(chat_id)
  if not os.path.exists('users.txt'):
    with open('users.txt', 'w') as f:
      pass
  with open('users.txt', 'r') as f:
    chats = f.read().splitlines()
  if chat_id not in chats:
    with open('users.txt', 'a') as f:
      f.write(chat_id + '\n')


# Til tanlash tugmalari
def get_language_keyboard():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  keyboard.add(
      types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz'),
      types.InlineKeyboardButton(
          '🇺🇿 Ўзбекча (Крил)', callback_data='lang_uz_kr'
      ),
      types.InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_ru'),
      types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en'),
  )
  return keyboard


# Guruhga qo'shish tugmasi (tilga moslashgan)
def get_group_keyboard(lang='uz'):
  keyboard = types.InlineKeyboardMarkup()
  btn_text = TEXTS.get(lang, TEXTS['uz'])['btn_group']
  add_btn = types.InlineKeyboardButton(
      text=btn_text, url='https://t.me/VideoSaveQualityBot?startgroup=true'
  )
  keyboard.add(add_btn)
  return keyboard


# --- 4. Buyruqlar va Til tanlash ---
@bot.message_handler(commands=['start'])
def start_message(message):
  save_chat_id(message.chat.id)
  bot.send_message(
      message.chat.id,
      '🇺🇿 Iltimos, tilni tanlang:\n🇷🇺 Пожалуйста, выберите язык:\n🇬🇧 Please'
      ' select a language:',
      reply_markup=get_language_keyboard(),
  )


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_callback(call):
  user_id = call.from_user.id
  if call.data == 'lang_uz_kr':
    lang_code = 'uz_kr'
  else:
    lang_code = call.data.replace('lang_', '')

  set_user_lang(user_id, lang_code)

  t = TEXTS.get(lang_code, TEXTS['uz'])
  bot.answer_callback_query(call.id, t['lang_changed'])
  bot.edit_message_text(
      t['welcome'],
      chat_id=call.message.chat.id,
      message_id=call.message.message_id,
      parse_mode='Markdown',
      reply_markup=get_group_keyboard(lang_code),
  )


# Bot guruhga qo'shilganda
@bot.my_chat_member_handler()
def bot_added_to_chat(message):
  new_status = message.new_chat_member.status
  if new_status in ['member', 'administrator']:
    save_chat_id(message.chat.id)


@bot.message_handler(commands=['stats'])
def stats_message(message):
  if message.from_user.id != ADMIN_ID:
    bot.reply_to(message, 'Kechirasiz, bu buyruq faqat admin uchun!')
    return

  if not os.path.exists('users.txt'):
    bot.reply_to(
        message, '📊 **Statistika:**\n\nJami chatlar (shaxsiy + guruh): 0 ta'
    )
    return

  with open('users.txt', 'r') as f:
    chats = f.read().splitlines()

  bot.reply_to(
      message,
      f'📊 **Bot statistikasi:**\n\nJami chatlar (shaxsiy + guruh): {len(chats)}'
      ' ta',
  )


# --- 5. Tarqatish funksiyasi (/send yoki /broadcast) ---
@bot.message_handler(
    content_types=['text', 'photo'],
    func=lambda message: message.from_user.id == ADMIN_ID
    and (
        (message.text and message.text.startswith('/send'))
        or (message.text and message.text.startswith('/broadcast'))
        or (message.caption and message.caption.startswith('/send'))
        or (message.caption and message.caption.startswith('/broadcast'))
    ),
)
def broadcast_message(message):
  if not os.path.exists('users.txt'):
    bot.reply_to(message, 'Hozircha bazada chatlar yo\'q.')
    return

  with open('users.txt', 'r') as f:
    chats = f.read().splitlines()

  if not chats:
    bot.reply_to(message, 'Baza bo\'sh.')
    return

  success = 0
  failed = 0

  if message.photo:
    file_id = message.photo[-1].file_id
    caption_text = message.caption or ''
    for cmd in ['/send', '/broadcast']:
      if caption_text.startswith(cmd):
        caption_text = caption_text.replace(cmd, '', 1).strip()

    markup = message.reply_markup if message.reply_markup else None

    for cid in chats:
      try:
        bot.send_photo(
            cid, file_id, caption=caption_text, reply_markup=markup
        )
        success += 1
      except Exception:
        failed += 1
  else:
    text = message.text or ''
    for cmd in ['/send', '/broadcast']:
      if text.startswith(cmd):
        text = text.replace(cmd, '', 1).strip()

    if not text:
      bot.reply_to(message, '⚠️ Matn yozmadingiz.')
      return

    markup = message.reply_markup if message.reply_markup else None

    for cid in chats:
      try:
        bot.send_message(cid, text, reply_markup=markup)
        success += 1
      except Exception:
        failed += 1

  bot.reply_to(
      message,
      f'Xabar tarqatildi! ✅\n\nYetib bordi: {success} ta chatga\nYetib'
      f' bormadi: {failed} ta',
  )


# --- 6. Video yuklash funksiyasi ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_all_messages(message):
  save_chat_id(message.chat.id)

  if message.chat.type in ['group', 'supergroup']:
    if not message.text:
      return
    text = message.text.strip()
    if not (text.startswith('http://') or text.startswith('https://')):
      return

  if not message.text:
    return

  text = message.text.strip()

  if text.startswith('http://') or text.startswith('https://'):
    lang = get_user_lang(message.from_user.id)
    t = TEXTS.get(lang, TEXTS['uz'])

    msg = bot.reply_to(message, t['downloading'])

    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text])

      with open('video.mp4', 'rb') as video:
        bot.send_video(
            message.chat.id,
            video,
            caption=f"{t['success']}{ADS_TEXT}",
            parse_mode='Markdown',
            reply_markup=get_group_keyboard(lang),
        )

      if os.path.exists('video.mp4'):
        os.remove('video.mp4')

      bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
      bot.edit_message_text(
          f'Xatolik yuz berdi: {e}', message.chat.id, msg.message_id
      )


# --- 7. Botni ishga tushirish ---
if __name__ == '__main__':
  print('Bot ishga tushdi...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)
