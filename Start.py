from telegram.ext import Updater, CommandHandler
from Handler import start, set_thumbnail, handle_upload, handle_download

def main():
    updater = Updater("YOUR_TOKEN_HERE")  # Creating an Updater instance with just the token
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("thumbnail", set_thumbnail))
    dp.add_handler(CommandHandler("upload", handle_upload))
    dp.add_handler(CommandHandler("dl", handle_download))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
