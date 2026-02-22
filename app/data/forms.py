from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import Optional, NumberRange

class CatalogFilterForm(FlaskForm):
    category = SelectField("Категория", choices=[("", "Все")], validators=[Optional()])
    min_price = DecimalField("Мин. цена", 
                           validators=[Optional(), NumberRange(min=0, message="Цена не может быть отрицательной")],
                           places=2)
    max_price = DecimalField("Макс. цена", 
                           validators=[Optional(), NumberRange(min=0, message="Цена не может быть отрицательной")],
                           places=2)
    sort_by = SelectField("Сортировка", choices=[
        ("name_asc", "Название ↑"),
        ("name_desc", "Название ↓"),
        ("price_asc", "Цена ↑"),
        ("price_desc", "Цена ↓"),
        ("quantity_asc", "Количество ↑"),
        ("quantity_desc", "Количество ↓"),  
        ("id_asc", "ID ↑"),
        ("id_desc", "ID ↓")
    ])
    submit = SubmitField("Применить фильтры")