from transitions import Machine


class Pizza(object):
    def __init__(self):
        self.answers = {}
        self.questions = [
            "Выбирите 'большую' или 'маленькую' . '/start'- начать заново ",
            "Выбирите 'наличкой' или 'безнал' . '/start'- начать заново",
            "Выбирите 'Да' или 'Нет'. '/start'- начать заново",
            "Спасибо за заказ. '/start'- начать заново",
            "/start - начать оформление нового заказа"
        ]
        self.ind = -1


make_pizza = Pizza()
states = ['start', 'size_selection', 'payment_method', 'check_order', 'order_is_accepted']

machine = Machine(model=make_pizza, states=states)


def handler(msg):
    msg = msg.lower()
    if msg == '/start':
        machine.set_state('start')
        machine.add_transition('tr_start', 'start', 'size_selection')
        make_pizza.tr_start()
        make_pizza.ind = 0
        return 'Какую вы хотите пиццу? Большую или маленькую?'

    elif (msg in ['большую', 'маленькую']) and make_pizza.is_size_selection():
        machine.add_transition('tr_size', 'size_selection', 'payment_method')
        make_pizza.tr_size()
        make_pizza.answers['size'] = msg
        make_pizza.ind = 1
        return 'Как вы будете платить? Наличкой или безнал'

    elif (msg in ['наличкой', 'безнал']) and make_pizza.is_payment_method():
        machine.add_transition('tr_payment', 'payment_method', 'check_order')
        make_pizza.tr_payment()
        make_pizza.answers['payment_method'] = msg
        make_pizza.ind = 2
        return f"Вы хотите {make_pizza.answers['size']} пиццу, оплата -{make_pizza.answers['payment_method']} ? "

    elif (msg in ['нет']) and make_pizza.is_check_order():
        return "/start - начать оформление нового заказа"

    elif (msg in ['да']) and make_pizza.is_check_order():
        machine.add_transition('tr_check', 'check_order', 'order_is_accepted')
        make_pizza.tr_check()
        make_pizza.ind = 3
        return "Спасибо за заказ. /start - начать заново"
    else:
        return make_pizza.questions[make_pizza.ind]

