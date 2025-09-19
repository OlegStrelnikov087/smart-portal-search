# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import app.database.crud as crud
from app.nlp import intent_classifier, entity_extractor, spell_checker
from app.search import search_engine
import json
import uuid
from pathlib import Path

# Создание приложения FastAPI
app = FastAPI(
    title="Smart Portal Search API",
    description="Умный поиск для Портала поставщиков Москвы",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Модели Pydantic
class SearchQuery(BaseModel):
    q: str

class FeedbackRequest(BaseModel):
    history_id: int
    is_positive: bool
    comment: Optional[str] = None

class HistoryItem(BaseModel):
    id: int
    original_query: str
    corrected_query: Optional[str]
    intent: Optional[str]
    entities: Optional[Dict[str, Any]]
    results_count: Optional[int]
    created_at: str

# Вспомогательные функции
def generate_action_url(action_type: str, entities: dict) -> str:
    """Генерация URL для действий с предзаполненными параметрами"""
    base_urls = {
        'tender': '/tender/create',
        'profile': '/profile/company/create',
        'signature': '/profile/signature/add',
        'company': '/profile/company/create'
    }
    
    if action_type not in base_urls:
        return None
    
    url = base_urls[action_type]
    params = []
    
    # Добавляем параметры из извлеченных сущностей
    if 'amount' in entities:
        params.append(f"amount={entities['amount']}")
    if 'product_name' in entities:
        from urllib.parse import quote
        params.append(f"product={quote(entities['product_name'])}")
    if 'document_number' in entities:
        params.append(f"number={entities['document_number']}")
    
    if params:
        url += '?' + '&'.join(params)
    
    return url

def format_search_results(results: List[Dict]) -> List[Dict]:
    """Форматирование результатов поиска для ответа"""
    formatted_results = []
    for result in results:
        formatted = {
            'id': result.get('id', ''),
            'title': result.get('title', ''),
            'content': result.get('content', '')[:200] + '...' if result.get('content') and len(result.get('content', '')) > 200 else result.get('content', ''),
            'type': result.get('type', ''),
            'score': float(result.get('score', 0)) if result.get('score') else 0
        }
        formatted_results.append(formatted)
    
    return formatted_results

# Endpoints API
@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Smart Portal Search API работает успешно!",
        "status": "OK",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/api/docs",
            "search": "/api/search (POST)",
            "history": "/api/history",
            "feedback": "/api/feedback (POST)",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Проверка статуса API и зависимостей"""
    dependencies = {
        "database": False,
        "nlp_models": False,
        "search_engine": False
    }
    
    try:
        # Проверка базы данных
        history = crud.get_history(limit=1)
        dependencies["database"] = True
    except:
        dependencies["database"] = False
    
    try:
        # Проверка NLP моделей
        test_text = "тестовый запрос"
        _ = spell_checker.correct_text(test_text)
        _ = intent_classifier.predict(test_text)
        _ = entity_extractor.extract_entities(test_text)
        dependencies["nlp_models"] = True
    except:
        dependencies["nlp_models"] = False
    
    try:
        # Проверка поискового движка
        _ = search_engine.search("тест", limit=1)
        dependencies["search_engine"] = True
    except:
        dependencies["search_engine"] = False
    
    return {
        "status": "healthy" if all(dependencies.values()) else "degraded",
        "service": "smart-portal-search",
        "dependencies": dependencies
    }

@app.post("/api/search")
async def search(query: SearchQuery):
    """Основной endpoint для обработки поисковых запросов"""
    try:
        # 1. Исправление опечаток
        corrected_query = spell_checker.correct_text(query.q)
        
        # 2. Классификация намерения
        intent_result = intent_classifier.predict(corrected_query)
        
        # 3. Извлечение сущностей
        entities = entity_extractor.extract_entities(corrected_query)
        
        # 4. Обработка в зависимости от намерения
        results = []
        action_url = None
        search_type = "all"
        
        if intent_result['intent'].startswith('search_'):
            # Поиск в соответствующем индексе
            search_type = intent_result['intent'].split('_')[1]
            if search_type == 'knowledge':
                results = search_engine.search(corrected_query, "knowledge")
            else:
                results = search_engine.search(corrected_query, "all")
        
        elif intent_result['intent'].startswith('create_'):
            # Генерация URL для действия
            action_type = intent_result['intent'].split('_')[1]
            action_url = generate_action_url(action_type, entities)
        
        # 5. Форматирование результатов
        formatted_results = format_search_results(results)
        
        # 6. Сохранение в историю
        history_id = crud.add_to_history(
            original_query=query.q,
            corrected_query=corrected_query,
            intent=intent_result['intent'],
            entities=entities,
            results_count=len(formatted_results)
        )
        
        # 7. Формирование ответа
        response = {
            "success": True,
            "data": {
                "original_query": query.q,
                "corrected_query": corrected_query,
                "intent": intent_result['intent'],
                "confidence": intent_result['confidence'],
                "entities": entities,
                "results": formatted_results,
                "action_url": action_url,
                "results_count": len(formatted_results),
                "search_type": search_type,
                "history_id": history_id
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Произошла ошибка при обработке запроса"
            }
        )

@app.get("/api/history")
async def get_history(limit: int = 20, offset: int = 0):
    """Получение истории поисковых запросов"""
    try:
        history = crud.get_history(limit, offset)
        
        # Преобразование entities из JSON строки в объект
        for item in history:
            if item.get('entities'):
                try:
                    item['entities'] = json.loads(item['entities'])
                except:
                    item['entities'] = {}
        
        return {
            "success": True,
            "data": {
                "history": history,
                "total": len(history),
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e)
            }
        )

@app.post("/api/feedback")
async def add_feedback(feedback: FeedbackRequest):
    """Добавление оценки к результатам поиска"""
    try:
        crud.add_feedback(
            feedback.history_id,
            feedback.is_positive,
            feedback.comment
        )
        
        return {
            "success": True,
            "message": "Оценка сохранена",
            "data": {
                "history_id": feedback.history_id,
                "is_positive": feedback.is_positive
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e)
            }
        )

@app.post("/api/test-add-history")
async def test_add_history(query: SearchQuery):
    """Тестовый endpoint для добавления в историю (для разработки)"""
    history_id = crud.add_to_history(
        original_query=query.q,
        corrected_query=query.q + " (исправлено)",
        intent="test_intent",
        entities={"test": "data", "amount": 100000},
        results_count=1
    )
    
    return {
        "success": True,
        "message": "Тестовая запись добавлена",
        "data": {
            "history_id": history_id,
            "query": query.q
        }
    }

# Frontend endpoints
@app.get("/ui")
async def read_root(request: Request):
    """Главная страница веб-интерфейса"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ui/history")
async def read_history(request: Request):
    """Страница истории запросов"""
    return templates.TemplateResponse("history.html", {"request": request})

# Обработчики ошибок
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {
        "success": False,
        "error": "Endpoint не найден",
        "path": request.url.path
    }

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return {
        "success": False,
        "error": "Внутренняя ошибка сервера",
        "message": "Попробуйте повторить запрос позже"
    }

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )