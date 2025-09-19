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

## 🚀 Быстрый старт

### Автоматическая установка:
```bash
git clone https://github.com/ваш-username/smart-portal-search.git
cd smart-portal-search
chmod +x setup.sh
./setup.sh
```

### Ручная установка:
```bash
git clone https://github.com/ваш-username/smart-portal-search.git
cd smart-portal-search
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python download_dependencies.py
uvicorn app.main:app --reload
```

### Доступные endpoints:
- 📄 API Docs: http://localhost:8000/docs
- 🌐 Web UI: http://localhost:8000/ui
- 🩺 Health: http://localhost:8000/api/health