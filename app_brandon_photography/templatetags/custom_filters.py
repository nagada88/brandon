from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def repeat(value, count):
    """
    Ismétli a megadott értéket a `count` számú alkalommal, különálló <span> elemekben.
    Példa: {{ '★'|repeat:3 }} => <span>★</span><span>★</span><span>★</span>
    """
    try:
        count = int(count)
        # Generálunk annyi <span>-t, ahány csillagot kérünk
        result = ''.join(f'<span>{value}</span>' for _ in range(count))
        return mark_safe(result)  # Biztonságos HTML visszaadás
    except (ValueError, TypeError):
        return ''