import unittest
import state_machine as fsm


def reset_storage(lst, n, st, ans='', size='', payment=''):
    for item in lst:
        if item['chat_id'] == n:
            item['fsm'].state = st
            item['answer'] = ans
            item['size'] = size
            item['payment'] = payment


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.ambry = fsm.Ambry()
        self.chat_id = 12345

    def test_start(self):
        ans = 'Какую вы хотите пиццу? Большую или маленькую?'
        self.ambry.put_in(self.chat_id, '/start')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_start_wrong(self):
        ans = '/start - начать оформление нового заказа'
        reset_storage(self.ambry.storage, self.chat_id, 'start', ans)
        self.ambry.put_in(self.chat_id, 'wrong_message')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_size(self):
        ans = 'Как вы будете платить? Наличкой или безнал'
        self.ambry.put_in(self.chat_id, 'большую')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans)
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_size_wrong(self):
        ans = "Выбирите 'большую' или 'маленькую' . '/start'- начать заново "
        self.ambry.put_in(self.chat_id, 'wrong_message')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans)
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_payment(self):
        ans = f"Вы хотите большую пиццу, оплата -наличкой ? "
        self.ambry.put_in(self.chat_id, 'наличкой')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans, 'большую', 'наличкой')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)


    def test_payment_wrong(self):
        ans = "Выбирите 'наличкой' или 'безнал' . '/start'- начать заново"
        self.ambry.put_in(self.chat_id, 'wrong_message')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans, 'большую', 'наличкой')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_order(self):
        ans = "Спасибо за заказ. /start - начать заново"
        self.ambry.put_in(self.chat_id, 'да')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans, 'большую', 'наличкой')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)

    def test_order_wrong(self):
        ans = "Выбирите 'Да' или 'Нет'. '/start'- начать заново"
        self.ambry.put_in(self.chat_id, 'wrong_message')
        reset_storage(self.ambry.storage, self.chat_id, 'size_selection', ans, 'большую', 'наличкой')
        self.assertEqual(self.ambry.show_answer(self.chat_id), ans)


if __name__ == '__main__':
    unittest.main()
