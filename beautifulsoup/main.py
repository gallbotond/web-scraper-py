from scrape_list import scrape_search_term

search_term = 'rtx 3060'
path, file = scrape_search_term(search_term)

print(f"Saved final data to {file}")