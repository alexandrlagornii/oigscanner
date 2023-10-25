from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Template for using oig scanner with firefox
def firefox_template(path_binary=None, path_driver=None):

    # Funcition that will hold the template with given paths
    def browser_template():

        # Set Options
        options = Options()
        if path_binary:
            options.binary_location = path_binary
        options.add_argument("--headless")

        # Set Service
        service = Service(path_driver)

        # Create browser instance and maximize
        browser = webdriver.Firefox(options=options, service=service)
        browser.maximize_window()

        # Return browser instance
        return browser

    # Return template for browser
    return browser_template