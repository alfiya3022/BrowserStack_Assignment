from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
import os


BASE_URL = "https://elpais.com"
OPINION_URL = "https://elpais.com/opinion/"


def get_opinion_links():
    print("Launching browser...")

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(BASE_URL)

        # Handle cookie popup if present
        try:
            accept_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Aceptar')]")
                )
            )
            accept_button.click()
        except Exception:
            pass

        driver.get(OPINION_URL)

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

        links = [article.get_attribute("href") for article in articles[:5]]

        print(f"Collected {len(links)} article links.")
        return links

    finally:
        driver.quit()
        print("Browser session closed.")


def scrape_article_details(url, index):
    print(f"\n[Article {index}] Fetching content...")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": BASE_URL
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch article {index}")
        return "Unavailable", ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

    # Extract first 10 paragraphs
    paragraphs = soup.find_all("p")
    content = "\n".join(
        p.get_text(strip=True) for p in paragraphs[:10]
    )

    # ---------- IMAGE EXTRACTION (ROBUST VERSION) ----------

    image_url = None

    # Try finding main image inside <figure>
    figure_tag = soup.find("figure")
    if figure_tag:
        img_tag = figure_tag.find("img")
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src")

    # Fallback to first image
    if not image_url:
        img_tag = soup.find("img")
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src")

    if image_url:

        # Handle relative URLs
        if image_url.startswith("/"):
            image_url = BASE_URL + image_url

        try:
            os.makedirs("images", exist_ok=True)

            img_response = requests.get(
                image_url,
                headers=headers,
                stream=True,
                timeout=10
            )

            if img_response.status_code == 200:

                file_path = f"images/article_{index}.jpg"

                with open(file_path, "wb") as file:
                    for chunk in img_response.iter_content(1024):
                        file.write(chunk)

                print("Image saved successfully.")

            else:
                print("Image request failed.")

        except Exception as e:
            print(f"Image download failed: {e}")

    return title, content
