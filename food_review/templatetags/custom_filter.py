from django import template

register = template.Library()

@register.filter(name='rupiah_format')
def rupiah_format(value):
    try:
        numeric_value = float(value)
        formatted_value = "{:,.0f}".format(numeric_value)
        return f"Rp {formatted_value}".replace(",", ".")
    except (ValueError, TypeError):
        return value