import telebot
import state_machine as fsm

bot = telebot.TeleBot('isert your token')


@bot.message_handler(content_types=['text'])
def get_answers(message):
    fsm.Ambry().put_in(message.chat.id, message.text)
    bot.send_message(message.chat.id, fsm.Ambry().show_answer(message.chat.id))


if __name__ == "__main__":
    bot.polling(none_stop=True)
