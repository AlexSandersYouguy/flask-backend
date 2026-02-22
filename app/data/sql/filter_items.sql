SELECT 
    p.id,
    p.sku,
    p.name,
    c.name as category_name,
    p.unit,
    p.price,
    COALESCE(ps.quantity, 0) as quantity
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN product_stock ps ON p.id = ps.product_id
WHERE 1=1
  {% if category %} AND c.name = '{{ category }}' {% endif %}
  {% if min_price %} AND p.price >= {{ min_price }} {% endif %}
  {% if max_price %} AND p.price <= {{ max_price }} {% endif %}
{% if sort_by == 'name_asc' %}
ORDER BY p.name ASC
{% elif sort_by == 'name_desc' %}
ORDER BY p.name DESC
{% elif sort_by == 'price_asc' %}
ORDER BY p.price ASC
{% elif sort_by == 'price_desc' %}
ORDER BY p.price DESC
{% elif sort_by == 'quantity_asc' %}
ORDER BY COALESCE(ps.quantity, 0) ASC
{% elif sort_by == 'quantity_desc' %}
ORDER BY COALESCE(ps.quantity, 0) DESC
{% elif sort_by == 'id_asc' %}
ORDER BY p.id ASC
{% elif sort_by == 'id_desc' %}
ORDER BY p.id DESC
{% else %}
ORDER BY p.name ASC
{% endif %};