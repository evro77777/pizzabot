import telebot
import state_machine as sm

bot = telebot.TeleBot('insert your token')


@bot.message_handler(content_types=['text'])
def get_answers(message):
    bot.send_message(message.from_user.id,
                     sm.handler(message.text))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
