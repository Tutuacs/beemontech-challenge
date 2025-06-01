import requests
from .models import Log, Quote
from bs4 import BeautifulSoup

page = 1
url = "https://quotes.toscrape.com/page/{}"

structure = [
    ['div', 'quote'],       # 0: top-level quote container
    ['span', 'text'],       # 1: quote text
    ['small', 'author'],    # 2: author name
    ['div', 'tags'],        # 3: tags container
    ['a', 'tag']            # 4: tag elements
]

def list(log=False):
    quotes = []
    struct = 0  # index to point to structure
    if log:
        Log.objects.create(message="Start of list", status='START_LIST')

    current_page = page
    while True:
        resp = fetch_page(current_page, log=log)
        if resp is None:
            if log:
                Log.objects.create(message=f"Failed to fetch page {current_page}", status='ERROR')
            break

        quotes_div = resp.find_all(structure[struct][0], class_=structure[struct][1])
        if not quotes_div:
            if log:
                Log.objects.create(message=f"No quotes found on page {current_page}", status='END_LIST')
            break

        q = 0
        for quote_div in quotes_div:
            quote = parse_quote(quote_div, current_page, struct, log=log)
            if quote:
                q += 1
                quotes.append(quote)
                if log:
                    Log.objects.create(message=f"Quote {q} on page {current_page} found successfully", status='PAGE')

        current_page += 1

    if log:
        Log.objects.create(message=f"Scraping finished with {len(quotes)} quotes", status='END_LIST')
    return quotes

def parse_quote(quote_div, page, struct, log=False):
    quote = None
    try:
        struct += 1
        text = quote_div.find(structure[struct][0], class_=structure[struct][1]).text
        struct += 1
        author = quote_div.find(structure[struct][0], class_=structure[struct][1]).text
        struct += 1
        tags_container = quote_div.find(structure[struct][0], class_=structure[struct][1])
        struct += 1
        tags = [
            t.text for t in 
            tags_container.find_all(
                structure[struct][0], class_=structure[struct][1]
            )
        ]

        quote = {
            'text': text,
            'author': author,
            'tags': ', '.join(tags),
            'page': page
        }

    except Exception as e:
        if log:
            Log.objects.create(message=f"Error parsing quote on page {page}: {e}", status='ERROR')
        return None

    return quote

def fetch_page(page, log=False):
    try:
        resp = requests.get(url.format(page))
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            if log:
                Log.objects.create(message=f"Fetched page {page} successfully", status='PAGE')
            return soup
        else:
            Log.objects.create(message=f"Failed to fetch page {page}, status code {resp.status_code}", status='ERROR')
            return None
    except Exception as e:
        Log.objects.create(message=f"Failed to request page {page}: {e}", status='ERROR')
        return None

def update_list(log=True):
    quotes = list(log=True)
    created_quotes = 0
    if quotes:
        for quote in quotes:

            exist = Quote.objects.filter(text=quote['text'], author=quote['author']).first()
            if exist:
                continue

            created_quote = Quote.objects.create(
                text=quote['text'],
                author=quote['author'],
                tags=quote['tags'],
                page=quote['page']
            )

            if not created_quote:
                Log.objects.create(
                    message=f"Error creating quote: {quote['text']}",
                    status='ERROR_CREATING'
                )
                continue
            created_quotes += 1
    return created_quotes