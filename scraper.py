# Import libraries
import requests
from bs4 import BeautifulSoup
import json

# Website settings
base_url = "https://quotes.toscrape.com"
page = 1
data = []

# Scrape all pages
while True:

    # Create URL for current page
    url = f"{base_url}/page/{page}/"

    print("\nScraping page:", page)
    print("URL:", url)

    # Send request and handle errors
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException:
        print("Error: Could not fetch the website.")
        break

    # Check response status
    print("Status code:", response.status_code)

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find quotes and authors
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")

    print("Quotes found:", len(quotes))

    # Store quotes and authors
    for quote, author in zip(quotes, authors):

        quote_text = quote.text.strip()
        author_text = author.text.strip()

        print("Quote:", quote_text)
        print("Author:", author_text)
        print()

        data.append({
            "quote": quote_text,
            "author": author_text
        })

    # Check for next page
    next_page = soup.find("li", class_="next")

    if next_page is None:
        print("No more pages.")
        break

    page += 1

# Display total quotes
print("\nTotal quotes scraped:", len(data))

# Save data to TXT file
with open("quotes.txt", "w", encoding="utf-8") as file:

    for item in data:
        file.write(item["quote"] + "\n")
        file.write("- " + item["author"] + "\n")
        file.write("\n")

print("Quotes saved successfully to quotes.txt")

# Save data to JSON file
with open("quotes.json", "w", encoding="utf-8") as file:

    json.dump(
        data,
        file,
        indent=4,
        ensure_ascii=False
    )

print("Quotes saved successfully to quotes.json")

# Project completed
print("\nWeb scraping completed successfully!")