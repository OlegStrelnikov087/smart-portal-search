# download_dependencies.py
import nltk
from pymorphy3 import MorphAnalyzer

def download_nltk_data():
    """Скачиваем необходимые данные для NLTK"""
    print("Скачивание данных NLTK...")
    nltk.download('stopwords')
    nltk.download('punkt')
    print("Данные NLTK успешно загружены.")

def init_pymorphy():
    """Инициализируем Pymorphy3 (он сам скачает словари при первом запуске)"""
    print("Инициализация Pymorphy3...")
    morph = MorphAnalyzer(lang='ru')
    print("Pymorphy3 успешно инициализирован.")
    return morph

if __name__ == "__main__":
    download_nltk_data()
    init_pymorphy()
    print("Все зависимости успешно загружены!")