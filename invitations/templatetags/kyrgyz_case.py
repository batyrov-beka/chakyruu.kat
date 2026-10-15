from django import template

register = template.Library()


@register.filter
def genitive_case(name):
    if not name:
        return ""

    name_str = str(name).strip()
    if not name_str:
        return ""

    last_char = name_str[-1].lower()

    vowels = ['а', 'э', 'е', 'о', 'ө', 'у', 'ү', 'ы', 'и', 'ю', 'я']
    voiced = ['б', 'в', 'г', 'д', 'ж', 'з', 'л', 'м', 'н', 'ң', 'р', 'й']

    is_soft = False
    for char in reversed(name_str.lower()):
        if char in ['э', 'е', 'ө', 'ү', 'и']:
            is_soft = True
            break
        elif char in ['а', 'о', 'у', 'ы', 'я', 'ю']:
            is_soft = False
            break

    if last_char in vowels:
        suffix = "нин" if is_soft else "нын"
    elif last_char in voiced:
        suffix = "дүн" if (is_soft and last_char in ['л', 'р']) else ("дин" if is_soft else "дын")
    else:
        suffix = "түн" if is_soft else "тын"

    if name_str.isupper():
        return f"{name_str}{suffix.upper()}"

    return f"{name_str}{suffix}"

MONTHS_KY = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

@register.filter
def kyrgyz_month(date_value):
    if not date_value:
        return ""
    try:
        return MONTHS_KY.get(date_value.month, "")
    except AttributeError:
        return ""