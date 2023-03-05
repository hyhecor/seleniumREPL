from selenium import webdriver
from selenium.webdriver.remote import webdriver as webdriver_

# browser = webdriver.Firefox()
# browser.get('http://selenium.dev/')


def SeleniumWebDriver(driverName: str) -> webdriver_.WebDriver:
    switch = {
        "firefox": webdriver.Firefox,
        "chrome": webdriver.Chrome,
        "safari": webdriver.Safari,
    }

    driver = switch.get(driverName.lower())

    return driver()


if __name__ == "__main__":
    SeleniumWebDriver("firefox")
