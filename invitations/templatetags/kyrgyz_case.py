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