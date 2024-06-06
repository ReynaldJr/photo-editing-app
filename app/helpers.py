import requests
from django.conf import settings


def search_image(search_query, quantity):
    url = f"https://api.unsplash.com/search/photos?client_id=hTL8A9nc-W5h1QxXMXKY-AP7froX23W0l01lRks4T60&query={search_query}&page=1&per_page={quantity}"

    response = requests.get(
        url=url
    )
    return response.json()