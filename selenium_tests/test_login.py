from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Налаштування Selenium WebDriver
options = Options()
# options.add_argument("--headless")  # Розкоментуй, якщо не хочеш бачити браузер
service = ChromeService()
driver = webdriver.Chrome(service=service, options=options)

# Тестові дані
BASE_URL = "http://127.0.0.1:8000"
VALID_EMAIL = "your_real_email@example.com"
VALID_PASSWORD = "your_real_password"
INVALID_EMAIL = "invalid@example.com"
INVALID_PASSWORD = "wrongpassword"

# Функції
BASE_URL = "http://127.0.0.1:8000"

def login(email, password):
    driver.get(f"{BASE_URL}/authentication/login/")  # <-- правильний шлях
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()


def logout():
    try:
        logout_button = driver.find_element(By.LINK_TEXT, "Logout")
        logout_button.click()
    except NoSuchElementException:
        print("Logout button not found.")

def is_logged_in():
    try:
        driver.find_element(By.LINK_TEXT, "Logout")
        return True
    except NoSuchElementException:
        return False

def has_error_message():
    try:
        return "Invalid credentials" in driver.page_source
    except Exception:
        return False

# ----------- ТЕСТ ------------

# 1. Login з валідними даними
login('rapid@gmail.com', 'zoloto')
time.sleep(4)
assert is_logged_in(), "Не вдалось увійти з правильними обліковими даними"
print("Успішний вхід з правильними даними")

# 2. Logout
logout()
time.sleep(4)
assert not is_logged_in(), "Вихід не спрацював"
print("Успішний вихід")

# 3. Login з невалідними даними
login('rapid@gmail.com', 'zopoto')
time.sleep(4)
assert not is_logged_in(), "Повинно бути відхилено вхід з неправильними даними"
assert has_error_message(), "Повідомлення про помилку відсутнє"
print("Невірні дані відхилені з повідомленням про помилку")

# Завершити
driver.quit()
