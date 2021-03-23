from requests_html import HTML, HTMLSession
from .models import Fragrance, URL
from utilities.email import send_email_using_gmail
import sys,json


# https://www.notino.es/franck-olivier/
# https://www.notino.es/salvatore-ferragamo/?f=1-1-131-55549
DEFAULT_PRICE = 999

NOTINO_URLS = [
    'https://www.notino.es/bentley/bentley-for-men-intense-eau-de-parfum-para-hombre/',
    'https://www.notino.es/rasasi/shuhrah-pour-homme-eau-de-parfum-para-hombre/',
    'https://www.notino.es/nautica/voyage-eau-de-toilette-para-hombre/',
    'https://www.notino.es/sean-john/unforgivable-men-eau-de-toilette-para-hombre/',
    'https://www.notino.es/lalique/encre-noire-sport-eau-de-toilette-para-hombre/',
    'https://www.notino.es/armaf/club-de-nuit-men-intense-eau-de-toilette-para-hombre/',
    'https://www.notino.es/mont-blanc/legend-spirit-eau-de-toilette-para-hombre/',
    'https://www.notino.es/versace/dreamer-eau-de-toilette-para-hombre/',
    'https://www.notino.es/lanvin/lhomme-eau-de-toilette-para-hombre/',
    'https://www.notino.es/hanae-mori/hm-eau-de-toilette-para-hombre/',
    'https://www.notino.es/versace/pour-homme-eau-de-toilette-para-hombre/',
    'https://www.notino.es/moschino/uomo-eau-de-toilette-para-hombre/',
    'https://www.notino.es/lacoste/eau-de-lacoste-l1212-blanc-eau-de-toilette-para-hombre/',
    'https://www.notino.es/davidoff/zino-eau-de-toilette-para-hombre/',
    'https://www.notino.es/jaguar/classic-gold-eau-de-toilette-para-hombre/',
    'https://www.notino.es/ferrari/bright-neroli-eau-de-toilette-unisex/',
    'https://www.notino.es/original-penguin/premium-blend-eau-de-toilette-para-hombre/',
    'https://www.notino.es/rasasi/tasmeem-men-eau-de-parfum-para-hombre/',
    'https://www.notino.es/lalique/encre-noire-alextreme-eau-de-parfum-para-hombre/',
    'https://www.notino.es/lalique/encre-noire-for-men-eau-de-toilette-para-hombre/',
    'https://www.notino.es/yves-saint-laurent/la-nuit-de-lhomme-eau-de-toilette-para-hombre/',
    'https://www.notino.es/dolce-gabbana/the-one-for-men-eau-de-parfum-para-hombre/',
    'https://www.notino.es/mont-blanc/legend-spirit-eau-de-toilette-para-hombre/',
    'https://www.notino.es/thierry-mugler/amen-pure-malt-eau-de-toilette-para-hombre/',
    'https://www.notino.es/prada/luna-rossa-carbon-eau-de-toilette-para-hombre/',
    'https://www.notino.es/jeanne-en-provence/acqua-eau-de-toilette-para-hombre/',
    'https://www.notino.es/mont-blanc/legend-eau-de-toilette-para-hombre/',
    'https://www.notino.es/abercrombie-fitch/fierce-colonia-para-hombre/',
    'https://www.notino.es/rochas/rochas-moustache-eau-de-parfum-para-hombre-125-ml/',
    'https://www.notino.es/rochas/rochas-man-eau-de-toilette-para-hombre/',
    'https://www.notino.es/mercedes-benz/mercedes-benz-intense-eau-de-toilette-para-hombre/',
    'https://www.notino.es/emanuel-ungaro/homme-iii-eau-de-toilette-para-hombre/',
    'https://www.notino.es/mandarina-duck/pure-black-eau-de-toilette-para-hombre/',
    'https://www.notino.es/jeanne-en-provence/olive-wood-juniper-eau-de-toilette-para-hombre/',
    'https://www.notino.es/franck-olivier/oud-touch-eau-de-parfum-para-hombre/',
    'https://www.notino.es/al-haramain/leather-oudh-eau-de-parfum-para-hombre/',
    'https://www.notino.es/michael-jordan/legend-colonia-para-hombre/',
    'https://www.notino.es/animale/animale-eau-de-toilette-para-hombre/',
    'https://www.notino.es/banana-republic/icon-collection-17-oud-mosaic-eau-de-parfum-unisex/',
    'https://www.notino.es/dirham/dirham-lote-de-regalo-i/',
    'https://www.notino.es/salvatore-ferragamo/uomo-eau-de-toilette-para-hombre/',
    'https://www.notino.es/salvatore-ferragamo/uomo-casual-life-eau-de-toilette-para-hombre/'

]

def save_urls_watched_to_json(file):
    print(file)
    with open(file, 'w') as f:
        json.dump(URL.urls, f)

def get_notino_urls():
    for qs in URL.objects.notino():
        yield qs.url



def scrape_fragrance_in_notino_html(html, url=''):
    e_offer = html.xpath('//div[@id="pdSelectedVariant"]//div[contains(text(), "Ofertas")]')
    is_in_offer = True if e_offer else False
    try:
        price = float(html.xpath('//div[@id="pd-price"]/span')[0].text.replace(',', '.'))
    except:
        price = DEFAULT_PRICE
    try:
        size = html.xpath('//*[@id="pdSelectedVariant"]/div[2]/div[1]/span/text()')
        if not size:
            size = html.xpath('//*[@id="pdSelectedVariant"]/div[1]/div[1]/span/text()')
        size = int(size[0])
    except:
        size = 0

    e = html.xpath('//div[@id="pdHeader"]/h1/span')
    try:
        name = e[1].text
        brand = e[0].text
        type_gender = e[2].text.split(' ')
        type_ = " ".join(type_gender[0:3])
        gender = " ".join(type_gender[3:])
        if 'mujer' in gender:
            gender = 'woman'
        elif 'hombre'in gender:
            gender = 'man'
    except:
        print('Error in: ', url)
        return {}
    return {
        'seller': 'Notino',
        'name': name,
        'brand': brand,
        'type': type_,
        'gender': gender,
        'size': size,
        'price': price,
        'is_in_offer': is_in_offer,
    }

def get_notino_fragrance_data(url):
    session = HTMLSession()
    res = session.get(url)
    html = res.html
    data = scrape_fragrance_in_notino_html(html, url)
    if data:
        data = {'url': url, **data}
    return data

def update_fragrances_db(data):
    fragrance, is_new_fragrance = Fragrance.objects.get_or_create(url=data.get('url'), defaults=data)
    if not is_new_fragrance:
        Fragrance.objects.filter(url=data.get('url')).update(**data)
        fragrance = Fragrance.objects.filter(url=data.get('url'))[0]
        fragrance.save()
        return fragrance

def get_notino_fragrance_data_and_update_fragrances_db(url):
    data = get_notino_fragrance_data(url)
    fragrance = update_fragrances_db(data)
    return fragrance

def get_notino_fragrances():
    session = HTMLSession()
    for url in get_notino_urls():
        res = session.get(url)
        html = res.html
        data = scrape_fragrance_in_notino_html(html, url)
        if data:
            data = {'url': url, **data}
            fragrance, is_new_fragrance = Fragrance.objects.get_or_create(url=data.get('url'), defaults=data)
            if not is_new_fragrance:
                Fragrance.objects.filter(url=data.get('url')).update(**data)
                fragrance = Fragrance.objects.filter(url=data.get('url'))[0]
                fragrance.save()


def print_fragrances(fragrances):
    for fragrance in fragrances:
        print(
            f'{fragrance.brand} {fragrance.name} {fragrance.size}ml {fragrance.price}€ ({fragrance.max_offer_price}€ - {fragrance.min_offer_price}€, {fragrance.min_price}€ - {fragrance.max_price}€) Is in offer: {fragrance.is_in_offer}:\n{fragrance.url}\n\n')


def get_cheaps_fragrances(fragrances):
    return [fragrance for fragrance in fragrances if fragrance.price <= 21]


def get_fragrances_in_offer(fragrances):
    return [fragrance for fragrance in fragrances if fragrance.is_in_offer]


def get_cheap_offers(fragrances):
    return [fragrance for fragrance in fragrances if (fragrance.is_in_offer and (
                fragrance.price <= 25 or fragrance.brand == 'Bentley' or fragrance.name == 'Encre Noire Sport'))]


def print_cheaps_fragrances(fragrances):
    cheapies = get_cheaps_fragrances(fragrances)
    print_fragrances(cheapies)


def print_fragrances_in_offer(fragrances):
    offer_fragrances = get_fragrances_in_offer(fragrances)
    print_fragrances(offer_fragrances)


def build_a_message_email_with_fragrance_offers(offers):
    msg = ''
    for offer in offers:
        try:
            offer.brand
        except:
            offer = Fragrance(**offer)
        msg = msg + f'{offer.brand} {offer.name} {offer.size}ml {offer.price}€  ({offer.max_offer_price}€ - {offer.min_offer_price}€, {offer.min_price}€ - {offer.max_price}€):\n{offer.url}\n\n'
    return msg


def build_a_subject_email_with_fragrance_offers(offers):
    fragrances = []
    for offer in offers:
        try:
            offer.brand
        except:
            offer = Fragrance(**offer)
        fragrances.append(f'{offer.brand} {offer.name} {offer.price}€')
    subject = ''
    if offers and len(offers) == 1:
        subject = 'Oferta de colonia: '
    elif offers:
        subject = 'Ofertas de colonias: '
    subject = subject + ', '.join(fragrances)
    return subject


def send_email_with_fragrances(fragrances, addressee):

    if fragrances  and addressee:
        msg = build_a_message_email_with_fragrance_offers(fragrances)
        subject = build_a_subject_email_with_fragrance_offers(fragrances)
        send_email_using_gmail('sexyscars555@gmail.com', [addressee], msg, subject)


def search_notino_offers_and_send_mail(addressee):
    fragrances = get_notino_fragrances()
    offers = get_cheap_offers(fragrances)
    if offers:
        send_email_with_fragrances(offers, addressee)
    else:
        print('Not offers found in Notino')


def get_notino_offers():
    fragrances = get_notino_fragrances()
    offers = get_fragrances_in_offer(fragrances)
    return offers


def get_notino_cheap_offers():
    fragrances = get_notino_fragrances()
    offers = get_cheap_offers(fragrances)
    return offers




shuhrah = {
    'name': 'Shuhrah Pour Homme',
    'brand': 'Rasasi',
    'type': 'Eau de Parfum para hombre',
    'url': 'https://www.notino.es/rasasi/shuhrah-pour-homme-eau-de-parfum-para-hombre/',
    'price': 31.50,
    'offer_price': 0,
    'is_in_offer': False,
    'seller': 'Notino',
}

if __name__ == '__main__':
    if (len(sys.argv) > 1 and sys.argv[1] == 'mail'):
        search_notino_offers_and_send_mail()
    if (len(sys.argv) > 1 and 'oferta' in sys.argv[1]):
        fragrances = get_notino_cheap_offers()
        print_fragrances(fragrances)
    else:
        fragrances = get_notino_fragrances()
        cheapies = get_cheaps_fragrances(fragrances)
        cheapy_offers = get_cheap_offers(fragrances)
        print_fragrances(cheapies)
