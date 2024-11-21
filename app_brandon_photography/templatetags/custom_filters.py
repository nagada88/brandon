from django import template

register = template.Library()

@register.filter
def repeat(value, count):
    """
    Ismétli a megadott értéket a `count` számú alkalommal.
    Példa: {{ '★'|repeat:3 }} => ★★★
    """
    try:
        count = int(count)
        return value * count
    except (ValueError, TypeError):
        return ''