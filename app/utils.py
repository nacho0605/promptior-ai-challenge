from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


import traceback


TIMEOUT = 10
RETRIES = 3
RETRIES_DELAY = 10


load_dotenv()


def get_element_by_xpath(web_driver, pattern):
    element = web_driver.find_element(By.XPATH, pattern)
    return element


def wait_for_elements_by_xpath(web_driver, timeout, pattern):
    elements = WebDriverWait(web_driver, timeout).until(
        expected_conditions.visibility_of_all_elements_located((By.XPATH, pattern))
    )
    return elements


def gather_services_context(web_driver, timeout, language, contact_link_text):
    get_element_by_xpath(web_driver, f"//div[contains(text(), '{language}')]").click()
    wait_for_elements_by_xpath(
        web_driver, timeout, f"//a[contains(text(), '{contact_link_text}')]"
    )[0].click()
    elements = wait_for_elements_by_xpath(
        web_driver, timeout, "//div[starts-with(@class, 'service-info')]"
    )
    services_context = "\n".join(
        [
            f"{element.find_element(By.CLASS_NAME, 'service-title').text}\n{element.find_element(By.CLASS_NAME, 'service-text').text}"
            for element in elements
        ]
    )
    return services_context


def gather_foundation_date_context(web_driver, timeout, language, about_text_keyword):
    get_element_by_xpath(web_driver, f"//div[contains(text(), '{language}')]").click()
    foundation_date_context = wait_for_elements_by_xpath(
        web_driver, timeout, f"//p[contains(text(), '{about_text_keyword}')]"
    )[0].text
    return foundation_date_context


def gather_promptior_context():

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    web_driver = webdriver.Chrome(options=options)

    promptior_context = ""

    for _ in range(RETRIES):

        try:
            base_url = "https://www.promptior.ai"
            language = "ES"

            web_driver.get(base_url)
            contact_link_text = "Contacto"
            services_context = gather_services_context(
                web_driver, TIMEOUT, language, contact_link_text
            )

            web_driver.get(f"{base_url}/about")
            about_text_keyword = "fundada"
            foundation_date_context = gather_foundation_date_context(
                web_driver, TIMEOUT, language, about_text_keyword
            )
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            services_context, foundation_date_context = "", ""
        finally:
            web_driver.quit()

        if all([services_context, foundation_date_context]):
            promptior_context = f"{services_context}\n\n{foundation_date_context}"
            break

        sleep(RETRIES_DELAY)

    return promptior_context

