from flask import Flask, render_template, request
import docx
import re # модуль для работы с регулярными выражениями

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/find_word', methods=['post', 'get'])
def find_word():
    if request.method == 'POST':  # Если запрос методом POST
        file = request.files['file']  # Получение загруженного файла
        if file and allowed_file(file.filename):  # Если файл допустимого формата
            filename = file.filename  # Получение имени файла
            if filename.endswith('.docx'):  # Если файл формата .docx
                doc = docx.Document(file)  # Создание объекта документа Word из файла
                words = []
                for para in doc.paragraphs:  # Для каждого абзаца в документе
                    words.extend(para.text.split())  # Добавление слов из абзаца в список слов
            elif filename.endswith('.txt'):  # Если файл формата .txt
                words = file.read().decode('utf-8').split()  # Чтение содержимого файла и разделение на слова
            else:
                return render_template('upload_file.html', error='Поддерживаются только файлы формата .docx и .txt') # Отображение сообщения об ошибке, если файл не допустимого формата
            words = [re.sub(r'[^\w\s]', '', word) for word in words if re.search(r'[a-zA-Zа-яА-Я]', word)] # Удаляем знаки препинания
            word_counts = {}
            for word in words:  # Для каждого слова в списке слов
                if word in word_counts:
                    word_counts[word] += 1  # Увеличение счетчика для этого слова
                else:
                    word_counts[word] = 1  # Добавление нового слова в словарь
            most_common_word = max(word_counts, key=word_counts.get)  # Нахождение слова с максимальным количеством повторений в словаре word_counts и присвоение его переменной most_common_word.
            return render_template('result.html', most_common_word=most_common_word)  # Отображение "result.html" и передача самого часто встречающегося слова в качестве аргумента.
        else:
            return render_template('upload_file.html', error='Поддерживаются только файлы формата .docx и .txt')
    return render_template('upload_file.html')

def allowed_file(filename):  # Функция, которая проверяет, является ли расширение загруженного файла допустимым.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx', 'txt'}

def run():
    app.run()