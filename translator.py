import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

TRANSLATE_URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"


def translate_to_english(text):
    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise EnvironmentError("RapidAPI credentials are not configured properly.")

    if not text:
        return ""

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    payload = {
        "from": "es",
        "to": "en",
        "text": text
    }

    try:
        response = requests.post(
            TRANSLATE_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        return data.get("trans", text)

    except requests.exceptions.RequestException as e:
        print(f"[Translation Error] {e}")
        return text
