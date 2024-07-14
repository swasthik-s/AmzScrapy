import requests
from bs4 import BeautifulSoup

def get_product_details_by_asin(asin):
    base_url = 'https://www.amazon.com/dp/'
    url = f'{base_url}{asin}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract product title
        product_name_element = soup.find('span', {'id': 'productTitle'})
        product_name = product_name_element.text.strip() if product_name_element else "Product title not found."

        # Extract product price
        price_element = soup.find('span', {'class': 'a-price-whole'})
        fraction_element = soup.find('span', {'class': 'a-price-fraction'})

        if price_element and fraction_element:
            price_whole = price_element.text.strip()
            price_fraction = fraction_element.text.strip()
            price = f"${price_whole}{price_fraction}"  # Correctly format the price
        else:
            price = "Price not found."

        # Extract brand name
        brand_element = soup.find('tr', class_='a-spacing-small po-brand')

        if brand_element:
            brand_td = brand_element.find_all('td')
            if len(brand_td) > 1:
                brand_name = brand_td[1].text.strip()
            else:
                brand_name = "Brand not found."
        else:
            brand_name = "Brand not found."

        return product_name, price, brand_name
    else:
        return "Failed to retrieve product page.", "", ""
