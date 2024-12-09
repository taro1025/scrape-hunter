from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import os
import logging
from twilio.rest import Client

TO_PHONE_NUMBER = os.environ["TO_PHONE_NUMBER"]
FROM_PHONE_NUMBER = os.environ["FROM_PHONE_NUMBER"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

url = "https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_movePage"

# Use headless mode
options = Options()
options.headless = True

# Set the path of the Firefox binary
firefox_binary_path = "/usr/bin/firefox-esr"
options.binary_location = firefox_binary_path

# Set the display port as an environment variable
display_port = os.environ.get("DISPLAY_PORT", "99")
display = f":{display_port}"
os.environ["DISPLAY"] = display

# Start the Xvfb server
xvfb_cmd = f"Xvfb {display} -screen 0 1024x768x24 -nolisten tcp &"
os.system(xvfb_cmd)

# Start the Firefox driver
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 20)  # Wait object to handle waiting for elements

def click_reserve_circle(driver):
    # Find the td element with onclick attribute containing 'selectDate' and click it
    reservable_td = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//td[contains(@onclick, 'selectDate') and contains(@class, 'enable')]")))
    actions = ActionChains(driver)
    logger.info("Found td element with onclick 'selectDate', scrolling to it")
    driver.execute_script("arguments[0].scrollIntoView(true);", reservable_td)
    actions.move_to_element(reservable_td).perform()
    logger.info("Scrolled to td element, clicking it")
    try:
        reservable_td.click()
        logger.info("reservable_td clicked")
        driver.save_screenshot("/app/assets/full_page_screenshot.png")
    except Exception as click_exception:
        logger.error("Standard click failed, trying JavaScript click: %s", click_exception)
        driver.execute_script("arguments[0].click();", reservable_td)
    logger.info("Current page URL: %s", driver.current_url)

try:
    # イベント一覧ページへ
    driver.get(url)
    logger.info("Current page URL: %s", driver.current_url)

    # Find the element containing the text "開始しました" and click it
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '猟銃等講習会')]")))
    # element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '開始しました')]")))
    element.click()
    logger.info("Click detail page")
    logger.info("Current page URL: %s", driver.current_url)

    # Find the checkbox and check it
    checkbox_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='reserveCaution']")))
    checkbox_label.click()
    logger.info("Check in reserveCaution")

    try:
        click_reserve_circle(driver)
    except:
        logger.error("Failed click circle svg")
        logger.info("Current page URL: %s", driver.current_url)
        raise "予約可能枠がなかったため終了"

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
      url="http://demo.twilio.com/docs/voice.xml",
      to=TO_PHONE_NUMBER
      from_=FROM_PHONE_NUMBER
    )

finally:
    # Close the browser
    driver.quit()
