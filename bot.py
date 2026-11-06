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

# --- 3. 4 Tildagi Matnlar va Reklama (Imzo) ---
TEXTS = {
    'uz': {
        'welcome': (
            '👋 **Salom! Xush kelibsiz!**\n\n'
            '🤖 **Bu bot nimalar qila oladi?**\n'
            '📥 Sizga quyidagi platformalardan video va rasmlarni yuqori sifatda'
            ' yuklab beradi:\n\n'
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
            '🛡 **Qo‘shimcha imkoniyatlar:**\n'
            '• Guruhdagi reklama va kirdi-chiqdi xabarlarini avtomatik'
            ' o‘chiradi!\n\n'
            '• *Videoni yuklab olish uchun istalgan platforma havolasini menga'
            " jo'nating*\n\n"
            '(Bot guruhlarda ham ishlaydi, guruhga qo‘shish uchun pastdagi'
            ' tugmani bosing 👇)'
        ),
        'btn_group': "➕ Guruhga qo'shish",
        'downloading': '⏳ Video yuklanmoqda, kuting...',
        'success': '✅ Muvaffaqiyatli yuklab olindi!',
        'ads': (
            '\n\n📥 **Yuklab olindi!**\n🤖 **Bot:** @VideoSaveQualityBot\n🛡'
            ' *Bu bot guruhdagi reklama hamda kirdi-chiqdi xabarlarini avtomatik'
            ' o‘chiradi!*'
        ),
        'wrong_link': (
            '⚠️ **Iltimos, to\'g\'ri havola yuboring!**\nSiz yuborgan matn'
            ' havola emas yoki qo\'llab-quvvatlanmaydigan manzil.'
        ),
    },
    'uz_kr': {
        'welcome': (
            '👋 **Салом! Хуш келибсиз!**\n\n'
            '🤖 **Бу бот нималар қила олади?**\n'
            '📥 Сизга қуйидаги платформалардан видео ва расмларни юқори сифатда'
            ' юклаб беради:\n\n'
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
            '🛡 **Қўшимча имкониятлар:**\n'
            '• Гуруҳдаги реклама ва кири-чиқди хабарларини автоматик'
            ' ўчиради!\n\n'
            '• *Видеони юклаб олиш учун исталган платформа ҳаволасини менга'
            " жўнатинг*\n\n"
            '(Бот гуруҳларда ҳам ишлайди, гуруҳга қўшиш учун пастдаги тугмани'
            ' босинг 👇)'
        ),
        'btn_group': '➕ Гуруҳга қўшиш',
        'downloading': '⏳ Видео юкланмоқда, кутинг...',
        'success': '✅ Муваффақиятли юклаб олинди!',
        'ads': (
            '\n\n📥 **Юклаб олинди!**\n🤖 **Бот:** @VideoSaveQualityBot\n🛡'
            ' *Бу бот гуруҳдаги реклама ҳамда кири-чиқди хабарларини автоматик'
            ' ўчиради!*'
        ),
        'wrong_link': (
            '⚠️ **Илтимос, тўғри ҳавола юборинг!**\nСиз юборган матн ҳавола эмас'
            ' ёки қўллаб-қувватланмайдиган манзил.'
        ),
    },
    'ru': {
        'welcome': (
            '👋 **Привет! Добро пожаловать!**\n\n'
            '🤖 **Что умеет этот бот?**\n'
            '📥 Помогает скачивать видео и фото в высоком качестве с следующих'
            ' платформ:\n\n'
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
            '🛡 **Дополнительные возможности:**\n'
            '• Автоматически удаляет рекламу и сообщения о входе/выходе в'
            ' группах!\n\n'
            '• *Отправьте мне ссылку на видео или фото для скачивания*\n\n'
            '(Бот также работает в группах, нажмите кнопку ниже, чтобы добавить'
            ' в группу 👇)'
        ),
        'btn_group': '➕ Добавить в группу',
        'downloading': '⏳ Загрузка видео, подождите...',
        'success': '✅ Успешно загружено!',
        'ads': (
            '\n\n📥 **Загружено!**\n🤖 **Bot:** @VideoSaveQualityBot\n🛡 *Этот'
            ' бот автоматически удаляет рекламу и сообщения о входе/выходе в'
            ' группах!*'
        ),
        'wrong_link': (
            '⚠️ **Пожалуйста, отправьте правильную ссылку!**\nОтправленный вами'
            ' текст не является ссылкой или поддерживаемым адресом.'
        ),
    },
    'en': {
        'welcome': (
            '👋 **Hello! Welcome!**\n\n'
            '🤖 **What can this bot do?**\n'
            '📥 Helps you download videos and photos in high quality from the'
            ' following platforms:\n\n'
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
            '🛡 **Additional features:**\n'
            '• Automatically deletes ads and join/leave messages in groups!\n\n'
            '• *Send me the link of any platform to download*\n\n'
            '(The bot also works in groups, click the button below to add it to'
            ' your group 👇)'
        ),
        'btn_group': '➕ Add to group',
        'downloading': '⏳ Downloading video, please wait...',
        'success': '✅ Successfully downloaded!',
        'ads': (
            '\n\n📥 **Downloaded!**\n🤖 **Bot:** @VideoSaveQualityBot\n🛡 *This'
            ' bot automatically deletes ads and join/leave messages in'
            ' groups!*'
        ),
        'wrong_link': (
            '⚠️ **Please send a valid link!**\nThe text you sent is not a link'
            ' or a supported address.'
        ),
    },
}


# Foydalanuvchi tilini aniqlash
def get_user_language(user):
  lang_code = user.language_code
  if not lang_code:
    return 'uz'
  lang_code = lang_code.lower()
  if 'uz' in lang_code:
    return 'uz'
  elif 'ru' in lang_code:
    return 'ru'
  elif 'en' in lang_code:
    return 'en'
  else:
    return 'uz'


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


# Guruhga qo'shish tugmasi
def get_group_keyboard(lang='uz'):
  keyboard = types.InlineKeyboardMarkup()
  btn_text = TEXTS.get(lang, TEXTS['uz'])['btn_group']
  add_btn = types.InlineKeyboardButton(
      text=btn_text, url='https://t.me/VideoSaveQualityBot?startgroup=true'
  )
  keyboard.add(add_btn)
  return keyboard


# --- 4. Start buyrug'i ---
@bot.message_handler(commands=['start'])
def start_message(message):
  save_chat_id(message.chat.id)
  lang = get_user_language(message.from_user)
  t = TEXTS.get(lang, TEXTS['uz'])

  bot.send_message(
      message.chat.id,
      t['welcome'],
      parse_mode='Markdown',
      reply_markup=get_group_keyboard(lang),
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


# --- 5. Guruhda Kirdi-Chiqdi va @PostBot xabarlarini tozalash ---
@bot.message_handler(
    content_types=[
        'new_chat_members',
        'left_chat_member',
        'text',
        'photo',
        'video',
        'document',
    ]
)
def group_cleaner_and_downloader(message):
  save_chat_id(message.chat.id)

  # 1. Kirdi-chiqdi xabarlarini o'chirish (guruhlarda)
  if message.chat.type in ['group', 'supergroup']:
    if message.new_chat_members or message.left_chat_member:
      try:
        bot.delete_message(message.chat.id, message.message_id)
      except Exception:
        pass
      return

    # 2. @PostBot orqali yuborilgan xabarlarni tekshirish
    if message.via_bot:
      if message.from_user.id != ADMIN_ID:
        try:
          bot.delete_message(message.chat.id, message.message_id)
        except Exception:
          pass
        return

    if not message.text:
      return
    text = message.text.strip()
    # Guruhda havoladan boshqa oddiy matn yozilsa, bot aralashmaydi (o'chirmaydi)
    if not (text.startswith('http://') or text.startswith('https://')):
      return

  if not message.text:
    return

  text = message.text.strip()
  lang = get_user_language(message.from_user)
  t = TEXTS.get(lang, TEXTS['uz'])

  # 3. Agar yuborilgan xabar havola bo'lmasa (oddiy matn yoki xato so'z bo'lsa)
  if not text.startswith('http://') and not text.startswith('https://'):
    bot.reply_to(message, t['wrong_link'], parse_mode='Markdown')
    return

  # 4. Havola bo'lsa video yuklash
  msg = bot.reply_to(message, t['downloading'])

  ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([text])

    with open('video.mp4', 'rb') as video:
      bot.send_video(
          message.chat.id,
          video,
          caption=f"{t['success']}{t['ads']}",
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


# --- 6. Tarqatish funksiyasi (/send yoki /broadcast) ---
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


# --- 7. Botni ishga tushirish ---
if __name__ == '__main__':
  print('Bot ishga tushdi...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)
