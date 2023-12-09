from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def firefox_template(path_binary: str = None, path_driver: str = None) -> templates:
    """Creates function that will hold options for firefox webdriver instances.

    Args:
        path_binary: path to firefox browser
        path_driver: path to geckodriver

    Returns:
        Function that creates firefox webdriver with given options
    """

    def browser_template() -> webdriver.Firefox:
        """Creates a firefox webdriver with given options.

        Returns:
            Firefox webdriver with given options
        """

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