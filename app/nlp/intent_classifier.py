# app/nlp/intent_classifier.py
import re
from typing import Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

class IntentClassifier:
    def __init__(self):
        self.pipeline = None
        self.intent_labels = {}
        self._initialize_intents()
        
    def _initialize_intents(self):
        """Инициализация предопределенных интентов и примеров"""
        self.intent_examples = {
            'create_tender': [
                "создай котировочную сессию",
                "хочу создать кс",
                "открой тендер на",
                "новая закупка",
                "создать закупку",
                "начать котировочную сессию"
            ],
            'search_tender': [
                "найди котировочные сессии",
                "покажи закупки",
                "ищу тендеры на",
                "поиск кс",
                "реестр котировок"
            ],
            'search_contract': [
                "найди контракты",
                "покажи заключенные договоры",
                "ищу контракты по",
                "реестр контрактов"
            ],
            'search_knowledge': [
                "как создать",
                "как добавить",
                "инструкция по",
                "помощь с",
                "как работает"
            ],
            'create_profile': [
                "создать профиль компании",
                "зарегистрировать организацию",
                "добавить новую компанию"
            ],
            'add_signature': [
                "добавить эцп",
                "установить электронную подпись",
                "добавить цифровую подпись"
            ]
        }
        
    def train(self):
        """Обучение классификатора на синтетических данных"""
        texts = []
        labels = []
        
        for intent, examples in self.intent_examples.items():
            for example in examples:
                texts.append(example)
                labels.append(intent)
        
        # Создаем pipeline с TF-IDF и LogisticRegression
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                lowercase=True,
                stop_words='russian',
                ngram_range=(1, 2),
                max_features=1000
            )),
            ('clf', LogisticRegression(
                random_state=42,
                max_iter=1000
            ))
        ])
        
        # Обучаем модель
        self.pipeline.fit(texts, labels)
        
    def predict(self, text: str) -> Dict:
        """Предсказание намерения для текста"""
        if self.pipeline is None:
            self.train()
            
        # Базовая предобработка
        processed_text = self._preprocess_text(text)
        
        # Предсказание
        intent = self.pipeline.predict([processed_text])[0]
        confidence = np.max(self.pipeline.predict_proba([processed_text]))
        
        return {
            'intent': intent,
            'confidence': float(confidence),
            'processed_text': processed_text
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Базовая предобработка текста"""
        text = text.lower().strip()
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def save_model(self, path: str = 'models/intent_classifier.joblib'):
        """Сохранение модели"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.pipeline, path)
    
    def load_model(self, path: str = 'models/intent_classifier.joblib'):
        """Загрузка модели"""
        if os.path.exists(path):
            self.pipeline = joblib.load(path)

# Синглтон экземпляр
intent_classifier = IntentClassifier()