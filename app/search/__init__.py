# app/search/__init__.py
"""
Модуль поиска и индексации
"""

from .whoosh_index import SearchEngine

__all__ = ['SearchEngine']