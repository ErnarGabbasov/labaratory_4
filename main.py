import unittest  # импортируем библиотеку для создания unit-тестов
from app import app  # импортируем Flask-приложение


class TestFindWord(unittest.TestCase):  # создаем класс для тестирования

    def test_index(self):  # тестируем функцию, которая отвечает за главную страницу
        tester = app.test_client(self)  # создаем клиент для тестирования
        response = tester.get('/')  # отправляем GET-запрос на главную страницу
        self.assertEqual(response.status_code, 200)  # проверяем, что код ответа равен 200

    def test_upload_page(self):  # тестируем функцию, которая отвечает за страницу загрузки файлов
        tester = app.test_client(self)
        response = tester.get('/find_word')  # отправляем GET-запрос на страницу загрузки файлов
        self.assertEqual(response.status_code, 200)  # проверяем, что код ответа равен 200

    def test_docx_file(self):  # тестируем функцию, которая отвечает за обработку .docx файлов
        tester = app.test_client(self)
        with open('test.docx', 'rb') as f:  # открываем тестовый .docx файл для чтения
            response = tester.post('/find_word', content_type='multipart/form-data', data={'file': f}) # отправляем POST-запрос на страницу загрузки файлов с тестовым .docx файлом
            self.assertIn('Самое частое слово в файле: "брат"', response.data.decode())  # проверяем, что полученный ответ содержит такой результат

    def test_txt_file(self):  # тестируем функцию, которая отвечает за обработку .txt файлов
        tester = app.test_client(self)  # создаем клиент для тестирования
        with open('test.txt', 'rb') as f:  # открываем тестовый .txt файл для чтения
            response = tester.post('/find_word', content_type='multipart/form-data', data={'file': f}) # отправляем POST-запрос на страницу загрузки файлов с тестовым .txt файлом
            self.assertIn('Самое частое слово в файле: "брат"', response.data.decode())  # проверяем, что полученный ответ содержит такой результат


if __name__ == '__main__':
    unittest.main()


