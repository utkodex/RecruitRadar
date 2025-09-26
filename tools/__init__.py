
"Keywords to linkedin link converter"
def fetch_linkedin_link(filter, keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(" ", "%20")
    link = f"https://www.linkedin.com/search/results/{filter.lower()}/?keywords={keyword}"
    return link