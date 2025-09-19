# app/search/whoosh_index.py
import os
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring
import pandas as pd
from typing import List, Dict
import json

class SearchEngine:
    def __init__(self, index_dir: str = "storage/whoosh_index"):
        self.index_dir = index_dir
        self.schema = Schema(
            id=TEXT(stored=True),
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            type=TEXT(stored=True),
            price=NUMERIC(stored=True),
            date=DATETIME(stored=True)
        )
        
    def create_index(self):
        """Создание индекса"""
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
        return index.create_in(self.index_dir, self.schema)
    
    def get_index(self):
        """Получение индекса"""
        if not index.exists_in(self.index_dir):
            return self.create_index()
        return index.open_dir(self.index_dir)
    
    def index_knowledge_base(self, csv_path: str):
        """Индексация базы знаний"""
        ix = self.get_index()
        writer = ix.writer()
        
        try:
            df = pd.read_csv(csv_path)
            for idx, row in df.iterrows():
                writer.add_document(
                    id=f"kb_{idx}",
                    title=str(row['question']),
                    content=str(row['answer']),
                    type="knowledge_base"
                )
            writer.commit()
        except Exception as e:
            print(f"Error indexing knowledge base: {e}")
            writer.cancel()
    
    def search(self, query_text: str, search_type: str = "all", limit: int = 10) -> List[Dict]:
        """Поиск по индексу"""
        ix = self.get_index()
        results = []
        
        with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
            if search_type == "knowledge":
                parser = QueryParser("content", ix.schema)
            else:
                parser = MultifieldParser(["title", "content"], ix.schema)
            
            query = parser.parse(query_text)
            search_results = searcher.search(query, limit=limit)
            
            for result in search_results:
                results.append(dict(result))
        
        return results

# Синглтон экземпляр
search_engine = SearchEngine()