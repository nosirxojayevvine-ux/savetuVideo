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


# Chatni (shaxsiy yoki guruhni) bazaga saqlash funksiyasi
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


# Inline tugma (Guruhga qo'shish)
def get_keyboard():
  keyboard = types.InlineKeyboardMarkup()
  add_btn = types.InlineKeyboardButton(
      text="➕ Guruhga qo'shish",
      url='https://t.me/VideoSaveQualityBot?startgroup=true',
  )
  keyboard.add(add_btn)
  return keyboard


# --- 3. Buyruqlar va Guruhga qo'shilishni ushlash ---


@bot.message_handler(commands=['start'])
def start_message(message):
  save_chat_id(message.chat.id)
  bot.send_message(
      message.chat.id,
      'Xush kelibsiz! Menga Instagram, TikTok yoki YouTube\'dan havola'
      ' yuboring.',
      reply_markup=get_keyboard(),
  )


# Bot guruhga qo'shilganda yoki chiqarib yuborilganda ishlaydi
@bot.my_chat_member_handler()
def bot_added_to_chat(message):
  new_status = message.new_chat_member.status
  if new_status in ['member', 'administrator']:
    chat_id = message.chat.id
    save_chat_id(chat_id)


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


# --- 4. Tarqatish funksiyasi (/send yoki /broadcast) ---
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

  # Rasm bilan bo'lsa
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
    # Faqat matnli bo'lsa
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


# --- 5. Guruhlar va shaxsiy chatlar uchun oddiy xabarlar / Video yuklash ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_all_messages(message):
  save_chat_id(message.chat.id)

  # Agar guruhda bo'lsa va oddiy matn yoki rasm bo'lsa, bot umuman aralashmaydi
  if message.chat.type in ['group', 'supergroup']:
    if not message.text:
      return
    text = message.text.strip()
    if not (text.startswith('http://') or text.startswith('https://')):
      return

  if not message.text:
    return

  text = message.text.strip()

  # Havola bo'lsa video yuklaydi
  if text.startswith('http://') or text.startswith('https://'):
    msg = bot.reply_to(message, '⏳ Video yuklanmoqda, kuting...')

    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text])

      with open('video.mp4', 'rb') as video:
        bot.send_video(
            message.chat.id,
            video,
            caption=f'Videoingizni yuklab berganimizdan mamnunmiz ❤️ va siga @VideoSaveQualityBot nomidan Raxmat, ketingi linklarda kutamiz.. !{ADS_TEXT}',
            parse_mode='Markdown',
            reply_markup=get_keyboard(),
        )

      if os.path.exists('video.mp4'):
        os.remove('video.mp4')

      bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
      bot.edit_message_text(
          f'Xatolik yuz berdi: {e}', message.chat.id, msg.message_id
      )


# --- 6. Botni ishga tushirish ---
if __name__ == '__main__':
  print('Bot ishga tushdi...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)
