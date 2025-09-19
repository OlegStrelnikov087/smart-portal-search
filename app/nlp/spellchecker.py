# app/nlp/spellchecker.py
from Levenshtein import distance
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
import re
from typing import List

class SpellChecker:
    def __init__(self):
        self.stop_words = set(stopwords.words('russian'))
        self.morph = MorphAnalyzer(lang='ru')
        self.dictionary = self._load_dictionary()
        
    def _load_dictionary(self) -> List[str]:
        """Загрузка словаря из базы знаний и часто используемых слов"""
        base_words = [
            'котировочная', 'сессия', 'кс', 'контракт', 'поставка',
            'закупка', 'тендер', 'профиль', 'эцп', 'подпись', 'электронная',
            'цифровая', 'создать', 'добавить', 'найти', 'показать',
            'канцелярские', 'товары', 'услуги', 'работы', 'оборудование',
            'москва', 'портал', 'поставщиков', 'заказчик', 'организация'
        ]
        return base_words
    
    def correct_text(self, text: str, max_distance: int = 2) -> str:
        """Исправление опечаток в тексте"""
        words = re.findall(r'\w+|[^\w\s]', text.lower())
        corrected_words = []
        
        for word in words:
            if not word.isalpha() or len(word) < 2:
                corrected_words.append(word)
                continue
                
            if word in self.stop_words:
                corrected_words.append(word)
                continue
                
            # Нормализуем слово для поиска в словаре
            normalized = self.morph.parse(word)[0].normal_form
            
            # Ищем наиболее похожее слово в словаре
            corrected_word = self._correct_word(normalized, max_distance)
            corrected_words.append(corrected_word if corrected_word else word)
        
        return ' '.join(corrected_words)
    
    def _correct_word(self, word: str, max_distance: int = 2) -> str:
        """Исправление одного слова"""
        if word in self.dictionary:
            return word
            
        best_match = None
        min_distance = float('inf')
        
        for correct_word in self.dictionary:
            dist = distance(word, correct_word)
            if dist < min_distance and dist <= max_distance:
                min_distance = dist
                best_match = correct_word
        
        return best_match if best_match else word

# Синглтон экземпляр
spell_checker = SpellChecker()