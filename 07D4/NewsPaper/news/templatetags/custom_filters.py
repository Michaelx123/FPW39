from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = ['1111', '2222', '3333']#словарь плохих слов.
    if isinstance(value, str):
        for bad in bad_words:
            value = value.replace(bad, '<BAD_WORD>')
        return value
    else:
        raise ValueError(f'Не является строкой: {type(value)}')
