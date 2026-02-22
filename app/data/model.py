from app.db.context_manager import DBContextManager
from app.db.sql_provider import SQLProvider 

class FetchModel:
    def __init__(self):
        self.sql_provider = SQLProvider('app/data/sql')
    
    def get_categories(self):
        """Получение списка уникальных категорий"""
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get("select_category.sql"))
                result = db.fetchall()
                
                categories = []
                for row in result:
                    categories.append({
                        'name': row[0]  # изменено с 'category' на 'name'
                    })
                
                return {'status': True, 'data': categories}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения категорий: {str(e)}', 'data': []}
    
    def get_products(self, params):
        """Получение товаров с фильтрацией"""
        translated = {
            "id": "ID",
            "sku": "Артикул",
            "name": "Название",
            "category_name": "Категория",
            "unit": "Единица измерения",
            "price": "Цена, руб.",
            "quantity": "В наличии",
        }
        try:
            # Валидация параметров
            validated_params = self._validate_product_params(params)
            
            # Получаем SQL с параметрами
            sql = self.sql_provider.get("filter_items.sql", **validated_params)
            
            with DBContextManager() as db:
                db.execute(sql)
                result = db.fetchall()
                
                # Получаем названия колонок
                columns = [translated[desc[0]] for desc in db.description]
                
                # Преобразуем в список словарей
                items = []
                for row in result:
                    item = {}
                    for i, col in enumerate(columns):
                        item[col] = row[i]
                    items.append(item)
                
                return {'status': True, 'data': items}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения товаров: {str(e)}', 'data': []}
    
    def _validate_product_params(self, params):
        """Валидация и нормализация параметров"""
        validated = {
            "category": params.get("category", "") or "",  # изменено с "material"
            "min_price": float(params.get("min_price", 0)) or 0,
            "max_price": float(params.get("max_price", 0)) or 0,
            "sort_by": params.get("sort_by", "name_asc") or "name_asc"
        }
        
        # Проверяем, что max_price >= min_price
        if validated["max_price"] > 0 and validated["max_price"] < validated["min_price"]:
            validated["max_price"] = 0 
        
        return validated