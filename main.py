from fastapi import FastAPI, HTTPException, Body
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pydantic import BaseModel
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

class CardData(BaseModel):
    card_name: str
    amount: float

class CardLoadData(BaseModel):
    id: str
    amount: float
    san: str

# Initialize WebDriver
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.page_load_strategy = "eager"

@app.post("/create-card/")
async def create_card(card_data: CardData):
    logging.info(f"Received data: card_name={card_data.card_name}, amount={card_data.amount}")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://banking.digitalexica.com/user.html")

        if "user.html" in driver.current_url:
            logging.info("Login page detected, performing login...")

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']")))

            username = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[1]/input")
            driver.execute_script("arguments[0].value='guy';", username)

            password = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[2]/input")
            driver.execute_script("arguments[0].value='Ninja2024!';", password)

            login_button = driver.find_element(By.XPATH, "//*[@id='loginForm']/input")
            login_button.click()

            WebDriverWait(driver, 10).until(EC.url_changes("https://banking.digitalexica.com/user.html"))
            logging.info(f"Current URL after login: {driver.current_url}")

        driver.get("https://banking.digitalexica.com/createcard.php")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "cardname")))

        card_name_field = driver.find_element(By.NAME, "cardname")
        card_name_field.send_keys(card_data.card_name)

        amount_field = driver.find_element(By.NAME, "amount")
        amount_field.send_keys(str(card_data.amount))

        bin_select = Select(driver.find_element(By.NAME, "bin"))
        bin_select.select_by_value("2")

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@value="Create"]')))
        create_button = driver.find_element(By.XPATH, '//input[@value="Create"]')
        create_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("managecards.php"))

        return {"status": "success", "message": "Card created successfully"}

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()



@app.post("/load-card/")
async def load_card(card_data: CardLoadData):
    # Log the incoming data for debugging purposes
    logging.info(f"Received data: Card Id={card_data.id}, amount={card_data.amount}, san={card_data.san}")


    # Initialize the WebDriver instance for each request
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://banking.digitalexica.com/user.html")

        # Check if we are on the login page
        if "user.html" in driver.current_url:
            logging.info("Login page detected, performing login...")

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']")))

            # Enter credentials and login
            username = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[1]/input")
            driver.execute_script("arguments[0].value='guy';", username)

            password = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[2]/input")
            driver.execute_script("arguments[0].value='Ninja2024!';", password)

            login_button = driver.find_element(By.XPATH, "//*[@id='loginForm']/input")
            login_button.click()

            # Wait for login completion
            WebDriverWait(driver, 10).until(EC.url_changes("https://banking.digitalexica.com/user.html"))
            logging.info(f"Current URL after login: {driver.current_url}")

        # Navigate to create card page
        driver.get(f"https://banking.digitalexica.com/loadcard.php?san={card_data.san}&id={card_data.id}")

        # Wait for page elements to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "amount")))

        # Fill in the card creation form with dynamic data
        card_name_field = driver.find_element(By.NAME, "amount")
        card_name_field.send_keys(card_data.amount)

        # Wait for the page to update (if required)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loadcard"]/input[3]')))

        # Click the create button
        create_button = driver.find_element(By.XPATH, '//*[@id="loadcard"]/input[3]')
        create_button.click()

        # Wait for a few seconds to observe the result
        WebDriverWait(driver, 10).until(EC.url_contains("managecards.php"))

        return {"status": "success", "message": "Card loaded successfully"}

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()


@app.post("/unload-card/")
async def load_card(card_data: CardLoadData):
    # Log the incoming data for debugging purposes
    logging.info(f"Received data: Card Id={card_data.id}, amount={card_data.amount}, san={card_data.san}")


    # Initialize the WebDriver instance for each request
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://banking.digitalexica.com/user.html")

        # Check if we are on the login page
        if "user.html" in driver.current_url:
            logging.info("Login page detected, performing login...")

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']")))

            # Enter credentials and login
            username = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[1]/input")
            driver.execute_script("arguments[0].value='guy';", username)

            password = driver.find_element(By.XPATH, "//*[@id='loginForm']/div[2]/input")
            driver.execute_script("arguments[0].value='Ninja2024!';", password)

            login_button = driver.find_element(By.XPATH, "//*[@id='loginForm']/input")
            login_button.click()

            # Wait for login completion
            WebDriverWait(driver, 10).until(EC.url_changes("https://banking.digitalexica.com/user.html"))
            logging.info(f"Current URL after login: {driver.current_url}")

        # Navigate to create card page
        driver.get(f"https://banking.digitalexica.com/unloadcard.php?san={card_data.san}&id={card_data.id}")

        # Wait for page elements to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "amount")))

        # Fill in the card creation form with dynamic data
        card_name_field = driver.find_element(By.NAME, "amount")
        card_name_field.send_keys(card_data.amount)

        # Wait for the page to update (if required)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="unloadcard"]/input[3]')))

        # Click the create button
        create_button = driver.find_element(By.XPATH, '//*[@id="unloadcard"]/input[3]')
        create_button.click()

        # Wait for a few seconds to observe the result
        WebDriverWait(driver, 10).until(EC.url_contains("managecards.php"))

        return {"status": "success", "message": "Card Unloaded successfully"}

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()