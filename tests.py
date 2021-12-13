import unittest
import state_machine as sm


class TestHandler(unittest.TestCase):

    def test_start(self):
        self.assertEqual(sm.handler('/start'), 'Какую вы хотите пиццу? Большую или маленькую?')

    def test_start_wrong(self):
        sm.machine.set_state('start')
        sm.make_pizza.ind = -1
        self.assertEqual(sm.handler('wrong_message'), '/start - начать оформление нового заказа')

    def test_size(self):
        sm.machine.set_state('size_selection')
        sm.make_pizza.ind = 0
        self.assertEqual(sm.handler('большую'), 'Как вы будете платить? Наличкой или безнал')

    def test_size_wrong(self):
        sm.machine.set_state('size_selection')
        sm.make_pizza.ind = 0
        self.assertEqual(sm.handler('wrong_message'), "Выбирите 'большую' или 'маленькую' . '/start'- начать заново ")

    def test_payment(self):
        sm.machine.set_state('payment_method')
        sm.make_pizza.ind = 1
        sm.make_pizza.answers['size'] = 'большую'
        sm.make_pizza.answers['payment_method'] = 'наличкой'
        self.assertEqual(sm.handler('наличкой'),
                         f"Вы хотите {sm.make_pizza.answers['size']} пиццу,"
                         f" оплата -{sm.make_pizza.answers['payment_method']} ? ")

    def test_payment_wrong(self):
        sm.machine.set_state('payment_method')
        sm.make_pizza.ind = 1
        self.assertEqual(sm.handler('wrong_message'),
                         "Выбирите 'наличкой' или 'безнал' . '/start'- начать заново")

    def test_order(self):
        sm.machine.set_state('check_order')
        sm.make_pizza.ind = 2
        self.assertEqual(sm.handler('да'),
                         "Спасибо за заказ. /start - начать заново")

    def test_order_wrong(self):
        sm.machine.set_state('check_order')
        sm.make_pizza.ind = 2
        self.assertEqual(sm.handler('wrong_message'),
                         "Выбирите 'Да' или 'Нет'. '/start'- начать заново")


if __name__ == '__main__':
    unittest.main()
