# app/nlp/__init__.py
"""
Модуль обработки естественного языка (NLP)
"""

from .intent_classifier import IntentClassifier
from .ner import EntityExtractor
from .spellchecker import SpellChecker

__all__ = ['IntentClassifier', 'EntityExtractor', 'SpellChecker']