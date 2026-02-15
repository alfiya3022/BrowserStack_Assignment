from scraper import get_opinion_links, scrape_article_details
from translator import translate_to_english
from text_analyzer import analyze_repeated_words

if __name__ == "__main__":
    print("Running main...")

    links = get_opinion_links()

    translated_titles = []
    
    for index, link in enumerate(links, start=1):
        print(f"\n{'='*50}")
        print(f"Processing Article {index}")
        print(f"Source URL: {link}")

        title, content = scrape_article_details(link, index)

        translated_title = translate_to_english(title)
        translated_titles.append(translated_title)

        print(f"\nOriginal Title (Spanish): {title}")
        print(f"Translated Title (English): {translated_title}")

