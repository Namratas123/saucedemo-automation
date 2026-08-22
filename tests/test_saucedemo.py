import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

# Small pauses to make the test easy to explain in the walkthrough video
DEMO_DELAY = 3


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver

    driver.quit()


def login(driver, username=USERNAME, password=PASSWORD):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    username_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )
    username_field.send_keys(username)

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "password")
        )
    )
    password_field.send_keys(password)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "login-button")
        )
    )
    login_button.click()

    wait.until(
        EC.url_contains("inventory.html")
    )

    time.sleep(DEMO_DELAY)


def test_valid_login(driver):
    login(driver)

    wait = WebDriverWait(driver, 10)

    title = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title")
        )
    )

    assert title.text == "Products"
    assert "inventory.html" in driver.current_url

    time.sleep(DEMO_DELAY)


def test_add_item_and_complete_checkout(driver):
    login(driver)

    wait = WebDriverWait(driver, 10)

    # --------------------------------------------------
    # Verify Products page
    # --------------------------------------------------

    title = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title")
        )
    )

    assert title.text == "Products"

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Add Sauce Labs Backpack
    # --------------------------------------------------

    add_to_cart = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    )

    add_to_cart.click()

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Open Cart
    # --------------------------------------------------

    cart_link = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
        )
    )

    cart_link.click()

    # Wait until the cart page is actually loaded
    wait.until(
        EC.url_contains("cart.html")
    )

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Verify Cart page
    # --------------------------------------------------

    cart_title = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title")
        )
    )

    assert cart_title.text == "Your Cart"

    # Verify selected product is in the cart
    product = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    assert product.text == "Sauce Labs Backpack"

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Checkout
    # --------------------------------------------------

    checkout_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "checkout")
        )
    )

    checkout_button.click()

    wait.until(
        EC.url_contains("checkout-step-one.html")
    )

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Verify Checkout Information page
    # --------------------------------------------------

    checkout_title = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title")
        )
    )

    assert checkout_title.text == "Checkout: Your Information"

    # --------------------------------------------------
    # Enter Customer Information
    # --------------------------------------------------

    first_name = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "first-name")
        )
    )

    first_name.send_keys("Namrata")

    time.sleep(1)

    last_name = driver.find_element(
        By.ID,
        "last-name"
    )

    last_name.send_keys("Sahu")

    time.sleep(1)

    postal_code = driver.find_element(
        By.ID,
        "postal-code"
    )

    postal_code.send_keys("492001")

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Continue to Overview
    # --------------------------------------------------

    continue_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "continue")
        )
    )

    continue_button.click()

    wait.until(
        EC.url_contains("checkout-step-two.html")
    )

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Verify Overview
    # --------------------------------------------------

    overview_title = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title")
        )
    )

    assert overview_title.text == "Checkout: Overview"

    overview_product = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    assert overview_product.text == "Sauce Labs Backpack"

    time.sleep(DEMO_DELAY)

    
    # Finish Order
    # --------------------------------------------------

    finish_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "finish")
        )
    )

    finish_button.click()

    wait.until(
        EC.url_contains("checkout-complete.html")
    )

    time.sleep(DEMO_DELAY)

    # --------------------------------------------------
    # Verify Order Confirmation
    # --------------------------------------------------

    confirmation = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    )

    assert confirmation.text == "Thank you for your order!"

    assert "checkout-complete.html" in driver.current_url

    time.sleep(DEMO_DELAY)


def test_locked_out_user_login(driver):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    # Enter locked-out username
    username_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "user-name")
        )
    )

    username_field.send_keys("locked_out_user")

    # Enter password
    password_field = driver.find_element(
        By.ID,
        "password"
    )

    password_field.send_keys(PASSWORD)

    time.sleep(DEMO_DELAY)

    # Click Login
    login_button = driver.find_element(
        By.ID,
        "login-button"
    )

    login_button.click()

    # Verify error message
    error_message = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='error']")
        )
    )

    assert "Sorry, this user has been locked out." in error_message.text

    time.sleep(DEMO_DELAY)