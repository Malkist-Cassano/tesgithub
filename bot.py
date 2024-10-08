import telebot
import os

api = "7077257623:AAEK5ERqGOJosJCI2hdq19sxCX1zXg2GZNc"
bot = telebot.TeleBot(api)

worker_file_path = 'worker.js'  # Path ke file worker.js

# Fungsi untuk menambahkan proxy
def add_proxy(path, proxy):
    with open(worker_file_path, 'r') as file:
        content = file.readlines()

    # Tambahkan proxy baru
    new_proxy_line = f'{{ path: \'{path}\', proxy: \'{proxy}\' }},\n'
    for i, line in enumerate(content):
        if line.startswith('const listProxy = ['):
            content.insert(i + 1, new_proxy_line)  # Tambahkan setelah baris listProxy
            break

    with open(worker_file_path, 'w') as file:
        file.writelines(content)

# Fungsi untuk menghapus proxy
def delete_proxy(path):
    with open(worker_file_path, 'r') as file:
        content = file.readlines()

    # Hapus proxy berdasarkan path
    new_content = []
    for line in content:
        if f"path: '{path}'" not in line:
            new_content.append(line)

    with open(worker_file_path, 'w') as file:
        file.writelines(new_content)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Selamat Datang!')

@bot.message_handler(commands=['addproxy'])
def handle_add_proxy(message):
    try:
        # Format perintah: /addproxy path proxy
        _, path, proxy = message.text.split()
        add_proxy(path, proxy)
        bot.reply_to(message, f'Proxy {path} ditambahkan dengan IP {proxy}')
    except Exception as e:
        bot.reply_to(message, f'Kesalahan: {str(e)}')

@bot.message_handler(commands=['deleteproxy'])
def handle_delete_proxy(message):
    try:
        # Format perintah: /deleteproxy path
        _, path = message.text.split()
        delete_proxy(path)
        bot.reply_to(message, f'Proxy {path} dihapus.')
    except Exception as e:
        bot.reply_to(message, f'Kesalahan: {str(e)}')

print('Bot berjalan dengan sukses')
bot.polling()