import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "autofill.profile_enabled": False,
    "autofill.credit_card_enabled": False
})

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:
    # Open website
    driver.get("https://adnabu-store-assignment1.myshopify.com/password")
    driver.maximize_window()

    #enter password
    password= driver.find_element(By.XPATH,"//input[@id='password']")
    password.send_keys("AdNabuQA")

    # clicking enter
    login_enter = driver.find_element(By.XPATH,"//button[text()='Enter']")
    login_enter.click()

    #Search product
    search_icon=driver.find_element(By.XPATH,"//details-modal[contains(@class,'header__search')]/descendant::summary/child::span")
    search_icon.click()

    ##search value
    search_value=wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='Search-In-Modal']")))
    search_value.send_keys("snow board")

    actions = ActionChains(driver)
    actions.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    #select product
    select_product=wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@id="CardLink--7801364676698"]')))
    select_product.click()

    #add to cart

    ##validating product is added to cart or not
    cart_pop_up = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@id="ProductSubmitButton-template--19850788667482__main"]')))
    cart_pop_up.click()

    ##checkout
    checkout_Product=wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="checkout"]')))
    checkout_Product.click()

    # --- Contact Section ---
    email = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email or mobile phone number']")))
    email.send_keys("testuser@gmail.com")

    # --- Country Dropdown ---
    country = Select(wait.until(EC.element_to_be_clickable((By.NAME, "countryCode"))))
    country.select_by_visible_text("United States")

    # --- Name Fields ---
    first_name = driver.find_element(By.NAME, "firstName")
    first_name.send_keys("Naren")

    last_name = driver.find_element(By.NAME, "lastName")
    last_name.send_keys("Raju")

    # --- Address ---
    address = driver.find_element(By.NAME, "address1")
    address.send_keys("123 Main Street")

    # Optional Apartment
    apartment = driver.find_element(By.NAME, "address2")
    apartment.send_keys("Apt 101")

    # --- City, State, ZIP ---
    city = driver.find_element(By.NAME, "city")
    city.send_keys("New York")

    state = Select(driver.find_element(By.NAME, "zone"))
    state.select_by_visible_text("New York")

    zip_code = driver.find_element(By.NAME, "postalCode")
    zip_code.send_keys("10001")

    # --- Checkbox ---
    save_info = driver.find_element(By.ID, "save_shipping_information")
    if not save_info.is_selected():
        save_info.click()

    # Wait for iframes to load
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print("Total iframes:", len(iframes))

    # -------- CARD NUMBER --------
    driver.switch_to.frame(iframes[0])
    card = wait.until(EC.visibility_of_element_located((By.NAME, "number")))
    card.send_keys("4242424242424242")
    driver.switch_to.default_content()

    # -------- EXPIRY --------
    driver.switch_to.frame(iframes[1])
    expiry = wait.until(EC.visibility_of_element_located((By.NAME, "expiry")))
    expiry.send_keys("12")
    expiry.send_keys("30")
    driver.switch_to.default_content()

    # -------- CVV --------
    driver.switch_to.frame(iframes[2])
    cvv = wait.until(EC.visibility_of_element_located((By.NAME, "verification_value")))
    cvv.send_keys("123")
    driver.switch_to.default_content()

    #--- payment ---
    paynow =driver.find_element(By.XPATH,'//button[@id="checkout-pay-button"]')
    paynow.click()

    # Validate error message
    error_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(),'doesn') or contains(text(),'valid card')]")
    ))

    assert "valid" in error_msg.text.lower() or "doesn" in error_msg.text.lower()

    # Screenshot
    allure.attach(driver.get_screenshot_as_png(),
                  name="Payment Failure",
                  attachment_type=AttachmentType.PNG)
    time.sleep(40)



except Exception as e:
    print("Test Failed:", str(e))

finally:
    driver.quit()