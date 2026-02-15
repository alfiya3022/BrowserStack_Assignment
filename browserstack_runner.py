import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from concurrent.futures import ThreadPoolExecutor

print("BrowserStack runner started...")

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"


def run_test(config):
    try:
        browser = config["browser"]
        print(f"\nStarting test: {config['name']}")

        if browser == "chrome":
            options = ChromeOptions()
        elif browser == "firefox":
            options = FirefoxOptions()
        elif browser == "edge":
            options = EdgeOptions()
        elif browser == "safari":
            options = SafariOptions()
        else:
            raise Exception("Unsupported browser")

        # Attach BrowserStack options
        options.set_capability("bstack:options", config["bstack_options"])

        driver = webdriver.Remote(
            command_executor=URL,
            options=options
        )

        print("Driver connected successfully.")

        driver.get("https://elpais.com/opinion/")

        articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

        print(f"{config['name']} - Found {len(articles)} articles.")

        driver.quit()

        print(f"{config['name']} completed successfully.")

    except Exception as e:
        print(f"Error in {config['name']}: {e}")


if __name__ == "__main__":

    print("\nStarting parallel execution...\n")

    configurations = [

        {
            "browser": "chrome",
            "name": "Windows Chrome Test",
            "bstack_options": {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Windows Chrome Test"
            }
        },
        
        {
            "browser": "firefox",
            "name": "Windows Firefox Test",
            "bstack_options": {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Windows Firefox Test"
            }
        },
        {
            "browser": "edge",
            "name": "Windows Edge Test",
            "bstack_options": {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Windows Edge Test"
            }
        },
        {
            "browser": "safari",
            "name": "macOS Safari Test",
            "bstack_options": {
                "os": "OS X",
                "osVersion": "Ventura",
                "sessionName": "macOS Safari Test"
            }
        },
        
        {
        "browser": "chrome",
        "name": "Android Mobile Test",
        "bstack_options": {
            "deviceName": "Samsung Galaxy S23",
            "realMobile": "true",
            "osVersion": "13.0",
            "sessionName": "Android Mobile Test"
            }
        },
        
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_test, configurations)

    print("\nAll tests completed.")




