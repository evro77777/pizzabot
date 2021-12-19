from transitions import Machine


class Ambry(object):
    data = set()
    storage = []

    @classmethod
    def put_in(cls, chat_id, text):
        if chat_id in cls.data:
            for item in cls.storage:
                if item['chat_id'] == chat_id:
                    item['text'] = text.lower()
                    Handler(item).change_state()
                    break
        else:
            obj = Handler({'chat_id': chat_id, 'fsm': FSM(), 'text': text.lower(),
                           'size': '', 'payment': '', 'answer': ''}).change_state()
            cls.storage.append(obj)
            cls.data.add(chat_id)

    @classmethod
    def show_answer(cls, chat_id):
        for item in cls.storage:
            if item['chat_id'] == chat_id:
                return item['answer']


class FSM(object):
    states = ['start', 'size_selection', 'payment_method', 'check_order', 'order_is_accepted']

    def __init__(self):
        self.machine = Machine(model=self, states=FSM.states, initial='start')
        self.machine.add_ordered_transitions(self.states)


class Handler(object):
    def __init__(self, data):
        self.data = data

    def change_state(self):
        if self.data['text'] == '/start':
            self.data['fsm'].machine.set_state('start')
            self.data['fsm'].next_state()
            self.data['answer'] = 'Какую вы хотите пиццу? Большую или маленькую?'
            return self.data

        elif (self.data['text'] in ['большую', 'маленькую']) and self.data['fsm'].state == 'size_selection':
            self.data['size'] = self.data['text']
            self.data['fsm'].next_state()
            self.data['answer'] = 'Как вы будете платить? Наличкой или безнал'
            return self.data

        elif (self.data['text'] in ['наличкой', 'безнал']) and self.data['fsm'].state == 'payment_method':
            self.data['payment'] = self.data['text']
            self.data['fsm'].next_state()
            self.data['answer'] = f"Вы хотите {self.data['size']} пиццу," \
                                  f" оплата -{self.data['payment']} ? "
            return self.data
        elif (self.data['text'] in ['нет']) and self.data['fsm'].state == 'check_order':
            self.data['answer'] = "/start - начать оформление нового заказа"
            return self.data
        elif (self.data['text'] in ['да']) and self.data['fsm'].state == 'check_order':
            self.data['fsm'].next_state()
            self.data['answer'] = "Спасибо за заказ. /start - начать заново"
            return self.data
        else:
            if self.data['fsm'].state == 'start':
                self.data['answer'] = "/start - начать оформление нового заказа"
                return self.data
            elif self.data['fsm'].state == 'size_selection':
                self.data['answer'] = "Выберите 'большую' или 'маленькую' . '/start'- начать заново "
                return self.data
            elif self.data['fsm'].state == 'payment_method':
                self.data['answer'] = "Выберите 'наличкой' или 'безнал' . '/start'- начать заново"
                return self.data
            elif self.data['fsm'].state == 'check_order':
                self.data['answer'] = "Выберите 'Да' или 'Нет'. '/start'- начать заново"
                return self.data
            else:
                self.data['answer'] = "/start - начать оформление нового заказа"
                return self.data

# t = Ambry()
# Ambry().put_in(12345,'/start')
# print(Ambry().show_answer(12345))
