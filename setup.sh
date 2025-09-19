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