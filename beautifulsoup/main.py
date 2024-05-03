from scrape_list import scrape_search_term

search_terms = ['Asus ROG flow x13', 'rtx 3060', 'rtx 3090', 'ryzen 9', 'ram 1x32gb']

for search_term in search_terms:
    path, file = scrape_search_term(search_term)
    print(f"Saved final data to {file}")