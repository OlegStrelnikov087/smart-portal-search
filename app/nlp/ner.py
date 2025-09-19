# app/nlp/ner.py
import re
from typing import Dict, List, Optional
from pymorphy3 import MorphAnalyzer
import numpy as np

class EntityExtractor:
    def __init__(self):
        self.morph = MorphAnalyzer(lang='ru')
        self.patterns = self._initialize_patterns()
        
    def _initialize_patterns(self):
        """Инициализация паттернов для извлечения сущностей"""
        return {
            'amount': [
                r'(\d+[\s\d]*)\s*(тыс|т\.р|тр|руб|рублей|₽)',
                r'(\d+[\s\d]*)\s*(тысяч|миллион|миллионов)',
            ],
            'product': [
                r'на\s+([^0-9]{5,}?)($|\s+\d|\s+на|руб)',
                r'поставк[ауе]\s+([^0-9]{5,}?)($|\s+\d)',
                r'закупк[ауе]\s+([^0-9]{5,}?)($|\s+\d)',
            ],
            'number': [
                r'№\s*(\d+)',
                r'номер\s+(\d+)',
                r'#\s*(\d+)'
            ]
        }
    
    def extract_entities(self, text: str) -> Dict:
        """Извлечение сущностей из текста"""
        entities = {}
        
        # Извлечение суммы
        amount_result = self._extract_amount(text)
        if amount_result:
            entities['amount'] = amount_result
        
        # Извлечение названия продукта/услуги
        product_result = self._extract_product(text)
        if product_result:
            entities['product_name'] = product_result
        
        # Извлечение номеров
        number_result = self._extract_number(text)
        if number_result:
            entities['document_number'] = number_result
        
        return entities
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """Извлечение денежной суммы"""
        for pattern in self.patterns['amount']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(' ', '')
                multiplier = 1
                
                # Определяем множитель
                if 'тыс' in match.group(2).lower() or 'т.р' in match.group(2).lower():
                    multiplier = 1000
                elif 'миллион' in match.group(2).lower():
                    multiplier = 1000000
                
                try:
                    amount = float(amount_str) * multiplier
                    return amount
                except ValueError:
                    continue
        
        return None
    
    def _extract_product(self, text: str) -> Optional[str]:
        """Извлечение названия продукта или услуги"""
        for pattern in self.patterns['product']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                product = match.group(1).strip()
                # Базовая нормализация
                product = re.sub(r'[^\w\s]', '', product)
                return product.title()
        
        return None
    
    def _extract_number(self, text: str) -> Optional[str]:
        """Извлечение номера документа"""
        for pattern in self.patterns['number']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return None

# Синглтон экземпляр
entity_extractor = EntityExtractor()