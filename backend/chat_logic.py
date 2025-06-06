def search_products(query, products):
    matched = []
    query = query.lower()
    for product in products:
        if query in product['name'].lower() or query in product['category'].lower():
            matched.append(product)
    # Use the enhanced sort
    sorted_matches = sort_books(matched, query)
    # Return top 5 with all fields
    return sorted_matches[:5]

def filter_by_genre(products, genre):
    return [product for product in products if product['category'].lower() == genre.lower()]

def filter_by_price_range(products, min_price, max_price):
    return [product for product in products if min_price <= float(product['price'].replace('₹', '').replace(',', '')) <= max_price]

def sort_by_rating(products):
    return sorted(products, key=lambda x: x.get('rating', 0), reverse=True)

def sort_books(books, query=None):
    def relevance(book):
        if not query:
            return 0
        q = query.lower()
        score = 0
        if q in book.get('name', '').lower():
            score += 3
        if q in book.get('category', '').lower():
            score += 2
        if book.get('bestseller', False):
            score += 1
        return score

    def price_value(book):
        try:
            return float(str(book.get('price', '0')).replace('₹', '').replace(',', ''))
        except Exception:
            return float('inf')

    return sorted(
        books,
        key=lambda b: (
            -relevance(b),
            not b.get('bestseller', False),
            -b.get('rating', 0),
            price_value(b)
        )
    )