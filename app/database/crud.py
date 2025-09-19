# app/database/crud.py
import sqlite3
import json
from pathlib import Path

# Указываем путь к базе данных
DATABASE_PATH = "storage/history.db"

def get_db_connection():
    """Создает и возвращает соединение с базой данных."""
    # Убедимся, что папка storage существует
    Path("storage").mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    # Чтобы получать словари вместо кортежей
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует базу данных, создает таблицы, если их нет."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Таблица для истории поиска
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_query TEXT NOT NULL,
            corrected_query TEXT,
            intent TEXT,
            entities TEXT, -- Будем хранить как JSON строку
            results_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER DEFAULT 1 -- Заглушка для демо
        )
    ''')

    # Таблица для оценок (feedback)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER,
            is_positive BOOLEAN,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (history_id) REFERENCES search_history (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_to_history(original_query, corrected_query, intent, entities, results_count=0):
    """Добавляет запрос в историю."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Преобразуем entities (словарь) в строку JSON для хранения
    entities_json = json.dumps(entities, ensure_ascii=False) if entities else None

    cursor.execute('''
        INSERT INTO search_history (original_query, corrected_query, intent, entities, results_count)
        VALUES (?, ?, ?, ?, ?)
    ''', (original_query, corrected_query, intent, entities_json, results_count))

    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def get_history(limit=20):
    """Получает последние записи истории."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM search_history
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))
    history = cursor.fetchall()
    conn.close()
    return [dict(item) for item in history]

def add_feedback(history_id, is_positive, comment=None):
    """Добавляет оценку к записи в истории."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (history_id, is_positive, comment)
        VALUES (?, ?, ?)
    ''', (history_id, is_positive, comment))
    conn.commit()
    conn.close()

# Инициализируем базу данных при импорте
init_db()