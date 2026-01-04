import telebot
from telebot import types

# KONFIGURASI
TOKEN = '8500940024:AAHHjJLNZaniVrlDn7D8nJ5gEPnKpgwsGCM'
ADMIN_ID = '7605498685' # Ganti dengan Chat ID kamu agar bot bisa kirim laporan pesanan
bot = telebot.TeleBot(TOKEN)

# --- DATA HARGA PASARAN ---
PRICING = {
    "web_toko": {"nama": "Web Toko Online (Full Fitur)", "harga": "Rp 1.500.000 - 3.500.000"},
    "web_company": {"nama": "Web Company Profile", "harga": "Rp 700.000 - 1.500.000"},
    "bot_toko": {"nama": "Bot Toko Otomatis (Integrasi Payment)", "harga": "Rp 500.000 - 1.200.000"},
    "bot_grup": {"nama": "Bot Manajemen Grup / Proteksi", "harga": "Rp 200.000 - 500.000"},
    "desain_ui": {"nama": "Desain UI/UX App/Web", "harga": "Rp 300.000 - 800.000"},
    "desain_logo": {"nama": "Desain Logo & Branding", "harga": "Rp 150.000 - 400.000"}
}

# --- MENU UTAMA ---
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🌐 Jasa Web', '🤖 Jasa Bot', '🎨 Jasa Desain', '📊 Testimoni')
    
    bot.send_message(message.chat.id, 
                     "👋 Selamat Datang di Asisten Digital!\n\nSilakan pilih kategori layanan di bawah untuk melihat detail dan harga pasaran:", 
                     reply_markup=markup)

# --- LOGIKA PILIHAN KATEGORI ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text == '🌐 Jasa Web':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Web Toko Online", callback_data="web_toko"))
        markup.add(types.InlineKeyboardButton("🏢 Web Company Profile", callback_data="web_company"))
        bot.send_message(chat_id, "Pilih jenis website yang Anda butuhkan:", reply_markup=markup)

    elif text == '🤖 Jasa Bot':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛍️ Bot Toko / Order", callback_data="bot_toko"))
        markup.add(types.InlineKeyboardButton("🛡️ Bot Grup / Admin", callback_data="bot_grup"))
        bot.send_message(chat_id, "Pilih jenis Bot Telegram yang Anda butuhkan:", reply_markup=markup)

    elif text == '🎨 Jasa Desain':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📱 Desain UI/UX", callback_data="desain_ui"))
        markup.add(types.InlineKeyboardButton("💎 Desain Logo", callback_data="desain_logo"))
        bot.send_message(chat_id, "Pilih layanan desain yang Anda butuhkan:", reply_markup=markup)
    
    elif text == '📊 Testimoni':
        bot.send_message(chat_id, "Silakan cek portofolio kami di: [Link Portofolio Anda]")

# --- LOGIKA TOMBOL LANJUTAN & NOTIFIKASI ADMIN ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in PRICING:
        item = PRICING[call.data]
        user = call.from_user
        
        # Kirim info ke pelanggan
        teks_user = (f"✅ **Pilihan Anda:** {item['nama']}\n"
                     f"💰 **Estimasi Harga:** {item['harga']}\n\n"
                     "Pesanan Anda telah diteruskan ke Admin. Silakan klik tombol di bawah untuk konsultasi langsung.")
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📲 Chat Admin (WhatsApp)", url="https://wa.me/6285179770547"))
        
        bot.edit_message_text(teks_user, call.message.chat.id, call.message.message_id, 
                              reply_markup=markup, parse_mode="Markdown")

        # KIRIM NOTIFIKASI KE TELEGRAM ANDA (ADMIN)
        teks_admin = (f"🔔 **PESANAN BARU MASUK!**\n\n"
                      f"👤 **Pelanggan:** {user.first_name} (@{user.username})\n"
                      f"📦 **Layanan:** {item['nama']}\n"
                      f"💵 **Range Harga:** {item['harga']}\n"
                      f"🆔 **User ID:** `{user.id}`")
        
        bot.send_message(ADMIN_ID, teks_admin, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Pesanan terkirim ke Admin!")

bot.infinity_polling()
