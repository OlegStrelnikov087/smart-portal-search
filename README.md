# 🚀 Smart Portal Search

Умная поисковая система для Портала поставщиков Москвы с обработкой запросов на естественном языке.

## ✨ Возможности

- 🔍 Поиск по базе знаний и реестрам
- 🤖 Обработка запросов на естественном языке
- 📝 Классификация намерений пользователя
- 🔧 Извлечение сущностей (суммы, продукты, номера)
- ✏️ Исправление опечаток
- 📊 История запросов и оценка результатов

## 🛠 Технологии

- **Backend**: FastAPI, Python 3.9+
- **NLP**: scikit-learn, pymorphy3, nltk
- **Поиск**: Whoosh
- **База данных**: SQLite
- **Обработка языка**: Natasha, Levenshtein

## ⚡ Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/smart-portal-search.git
cd smart-portal-search

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Загрузка NLP зависимостей
python download_dependencies.py

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000