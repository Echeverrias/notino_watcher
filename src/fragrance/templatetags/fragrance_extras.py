from django import template

register = template.Library()

UNKNOWN_PRICE = 900
@register.filter(name='stringify')
def stringify(fragrance):
    return f'{fragrance.brand} {fragrance.name} Eau de {fragrance.type} pour {fragrance.gender} {"?" if fragrance.size == 0 else fragrance.size}ml {"?" if fragrance.price >= UNKNOWN_PRICE else fragrance.price}€ {" in offer" if fragrance.is_in_offer else ""} ({"?" if fragrance.max_offer_price >= UNKNOWN_PRICE else fragrance.max_offer_price}€-{"?" if fragrance.min_offer_price >= UNKNOWN_PRICE else fragrance.min_offer_price}€, {"?" if fragrance.min_price >= UNKNOWN_PRICE else fragrance.min_price}€-{"?" if fragrance.max_price >= UNKNOWN_PRICE else fragrance.max_price}€)'
