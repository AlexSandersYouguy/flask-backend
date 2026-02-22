from flask import Blueprint, render_template, request
from app.data.forms import CatalogFilterForm
from app.data.model import FetchModel
from app.auth.access import login_required

data = Blueprint("data", __name__, template_folder="templates")
fetch_model = FetchModel()

@data.route("/", methods=["GET"])
@login_required
def index():
    return render_template("monitoring.html", title="Мониторинг данных")

@data.route("/catalog", methods=["GET", "POST"])
@login_required
def catalog():
    form = CatalogFilterForm()
    items = []
    columns = []
    
    # Получаем доступные категории для выпадающего списка
    category_result = fetch_model.get_categories()
    if category_result['status']:
        form.category.choices = [("", "Все")] + [(c['name'], c['name'])  # изменено с material на category
                                                for c in category_result['data']]
    
    
    if request.method == "POST":
        # Собираем параметры фильтрации из формы
        filter_params = {
            "category": form.category.data or "",
            "min_price": float(form.min_price.data) if form.min_price.data else 0,
            "max_price": float(form.max_price.data) if form.max_price.data else 0,
            "sort_by": form.sort_by.data or "name_asc"
        }
    
        # Получаем товары с фильтрацией
        result = fetch_model.get_products(filter_params)
        
        if result['status']:
            items = result['data']
            if items:
                columns = list(items[0].keys())  # Получаем названия колонок из первого элемента
        
    return render_template("catalog.html", 
                         form=form, 
                         items=items, 
                         columns=columns,
                         title="Каталог продуктов")