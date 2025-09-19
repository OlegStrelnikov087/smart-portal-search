# app/database/__init__.py
"""
Модуль работы с базой данных
"""

from .crud import (
    get_db_connection,
    init_db,
    add_to_history,
    get_history,
    add_feedback
)

__all__ = [
    'get_db_connection',
    'init_db',
    'add_to_history',
    'get_history',
    'add_feedback'
]