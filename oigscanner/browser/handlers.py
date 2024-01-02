import os
import re
import pandas as pd

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from typing import Callable


class browser_wrapper:

    def __init__(
        self,
        browser_template: Callable[[], WebDriver],
        wait_time: int = 10,
        timeout: int = 20
        ):
        """Set reference to an instance of a webdriver. Set time to wait for an html element. Set timout.

        Args:
            browser_template: webdriver template
            wait_time: time to wait for an element to be found
            timout: time to wait if nothing is happening
        """

        # Set browser template, wait time, timeout
        self.BROWSER_TEMPLATE = browser_template
        self.WAIT_TIME = wait_time
        self.TIMEOUT = timeout

        # Create browser
        self.create_browser()


    def __del__(self) -> None:
        """Closes webdriver instance."""
        self.BROWSER.quit()


    def create_browser(self) -> None:
        """Creates an instance of a webdriver with given options"""

        # Set browser
        self.BROWSER = self.BROWSER_TEMPLATE()

        # Set wait time
        self.WAIT = WebDriverWait(self.BROWSER, self.WAIT_TIME)

        # Set timout time
        self.BROWSER.set_page_load_timeout(self.TIMEOUT)


    def quit(self) -> None:
        "Close browser thus quitting webdriver."
        self.BROWSER.quit()

    
    def get(self, page: str) -> None:
        """Opens with the browser given page.
        
        Args:
            page: URL of the page
        """
        self.BROWSER.get(page)


    def back(self) -> None:
        "Goes back to the previous page."
        self.BROWSER.back()

    
    def create_log_entry(self, entry: str) -> None:
        """Creates log entry.

        Args:
            entry: string to write into log file
        """

        log_file_name = "logs.txt"
        with open(log_file_name, "a+", encoding="utf-8") as log:
            log.write(entry)


    def check_exists(
        self,
        element_name: str,
        attribute: str
        ) -> bool:
        """Checks if element exists and returns true if it does, otherwise false.
        
        Args:
            element_name: name of an html element
            attribute: specifies html 
            
        Returns:
            True if found given element, False if not
        """

        try:
            self.BROWSER.find_element(attribute, element_name)
        except NoSuchElementException:
            return False
        return True


    def enter_value(
        self,
        element_name: str,
        attribute: str,
        value: str
        ) -> None:
        """Enters the value into the field given the name of an element and the attribute.
        
        Args:
            element_name: name of an html element
            attribute: specifies html attribute
            value: value that we will enter into the field
        """

        # Find and wait until it's clickable
        element = self.WAIT.until(EC.element_to_be_clickable((attribute, element_name)))
        
        # Enter the value
        element.click()
        element.clear()
        element.send_keys(value)


    def click_when_clickable(
        self,
        element_name: str,
        attribute: str
        ) -> None:
        """Click on an element when possible with given attribute.
        
        Args:
            element_name: name of an html element
            attribute: specifies html attribute
        """

        # Find
        element = self.WAIT.until(EC.element_to_be_clickable((attribute, element_name)))
    
        # Click
        element.click()


    def take_screenshot(
        self,
        element_name: str,
        attribute: str,
        path_screenshot: str
        ) -> None:
        """Takes a screenshot of an element given element name, attribute, and a path to the screenshot.
        
        Args:
            element_name: name of an html element
            attribute: specifies html attribute
            path_screenshot: path of an image that will be taken
        """

        # Find
        element = self.WAIT.until(EC.visibility_of_element_located((attribute, element_name)))   

        # Take a screenshot
        element.screenshot(path_screenshot)


    def find_unique_path_screenshot(self, path_screenshot: str) -> str:
        """Checks if there is a screenshot with the same name and adds number to the name if there is.
        
        Args:
            path_screenshot: path of a screenshot

        Returns:
            Unique screenshot path if found, False if not
        """

        # Number to append to copy
        i = 1

        # Search for duplicates
        while os.path.isfile(path_screenshot):

            # Remove file format
            path_screenshot = path_screenshot.removesuffix(".png")

            # Remove brackets with numbers
            pattern = r"\(\d*?\)"
            path_screenshot = re.sub(pattern, "", path_screenshot)

            # Remove white space
            path_screenshot = path_screenshot.strip()
            
            # Make new name
            path_screenshot += "(" + str(i) + ")"
            path_screenshot += ".png"

            # Increase copy counter
            i +=1

        return path_screenshot


class oig_scanner(browser_wrapper):

    def __init__(
        self,
        browser_template: Callable[[], WebDriver],
        wait_time: int = 10,
        timeout: int = 20,
        ):
        """Opens the browser and gets the oig exclusions site.
        
        Args:
            browser_template: webdriver template
            wait_time: time to wait for an element to be found
            timout: time to wait if nothing is happening
        """

        # Initialize using parent (browser_wrapper)
        super().__init__(browser_template, wait_time, timeout)


    def get_individuals_page(self) -> None:
        """Gets first page of oig exclusions site."""
        self.get("https://exclusions.oig.hhs.gov")


    def get_entities_page(self) -> None:
        """Gets first page of oig exclusions site and sets searching for entities."""
        self.get("https://exclusions.oig.hhs.gov")
        self.click_when_clickable("ctl00_cpExclusions_Linkbutton1", By.ID)


    def take_oig_screenshot(
        self,
        data: pd.Series,
        month: str,
        year: int
        ) -> None:
        """Takes a screenshot of an individual or entity page.

        Args:
            data: last name and first name or entity name in pandas series.
            month: month to append to the name of the screenshot
            year: year to append to the name of the screenshot
        """

        def individual_take_screenshot(last_name: str, first_name: str) -> None:
            """Helper function that takes a screenshot of an individual.
            
            Args:
                last_name: last name of the individual.
                first_name: first name of the individual
            """

            # Print individual
            print(f"{last_name} , {first_name}")

            # Try to make a screenshot (5 tries for if something wrong)
            for i in range(5):

                try:
                    # Check if page loaded correctly
                    exists_last_name = self.check_exists("ctl00$cpExclusions$txtSPLastName", By.NAME)
                    exists_first_name = self.check_exists("ctl00$cpExclusions$txtSPFirstName", By.NAME)
                    if not exists_last_name or not exists_first_name:
                        self.get_individuals_page()
                        continue

                    # Enter last name and first name
                    self.enter_value("ctl00$cpExclusions$txtSPLastName", By.NAME, last_name)
                    self.enter_value("ctl00$cpExclusions$txtSPFirstName", By.NAME, first_name)

                    # Check if fields are not empty and values are correct
                    last_name_field = self.BROWSER.find_element(By.NAME, "ctl00$cpExclusions$txtSPLastName").get_attribute("value")
                    first_name_field = self.BROWSER.find_element(By.NAME, "ctl00$cpExclusions$txtSPFirstName").get_attribute("value")
                    if last_name_field != last_name or first_name_field != first_name:
                        self.get_individuals_page()
                        continue

                    # Find and press the search button
                    self.click_when_clickable("ctl00$cpExclusions$ibSearchSP", By.NAME)

                    # Check if next page loaded
                    next_page = self.check_exists("SP", By.ID)
                    if (not next_page):
                        self.get_individuals_page()
                        continue
                    
                    # Check if results were found for the individual or not
                    check = self.check_exists("ctl00_cpExclusions_pnlEmpty", By.ID)
                    
                    # Check if folder exists for screenshots and create it if needed
                    if (os.path.exists("screenshots_individuals/") == False):
                        os.makedirs("screenshots_individuals")
                    
                    # Create screenshot path
                    path_screenshot = f"screenshots_individuals/{str(last_name)} {str(first_name)} OIG {str(month)} {str(year)}"
                    path_screenshot = path_screenshot.strip()
                    if not check:
                        path_screenshot += " CHECK"
                    path_screenshot += ".png"

                    # Find unique screenshot path and make a screenshot
                    unique_path_screenshot = self.find_unique_path_screenshot(path_screenshot)
                    self.take_screenshot("content", By.ID, unique_path_screenshot)
                    
                    # Return to the search page
                    self.back()

                    # Exit loop
                    break

                except Exception as e:
                    print("-------------------------EXCEPTION OCCURED-----------------------------")
                    print(str(e))
                    print("---------------------------TRYING AGAIN--------------------------------")
                    try:
                        self.quit()
                    except NoSuchWindowException:
                        pass
                    self.create_browser()

            else:
                log_entry = f"Failed for - {last_name} {first_name}\n"
                print(log_entry)
                self.create_log_entry(log_entry)


        def entity_take_screenshot(entity: str) -> None:
            """Helper function that takes a screenshot of an entity given its name.

            Args:
                entity: name of the entity

            Returns:
                True if able to take screenshot, otherwise false
            """

            # Print entity
            print(entity)

            # Try to make a screenshot (5 tries for if something wrong)
            for i in range(5):

                try:
                    # Check if page loaded correctly
                    exists_entity = self.check_exists("ctl00$cpExclusions$txtSBName", By.NAME)
                    if not exists_entity:
                        self.get_entities_page()
                        continue

                    # Enter entity name
                    self.enter_value("ctl00$cpExclusions$txtSBName", By.NAME, entity)

                    # Check if fields are not empty
                    entity_field = self.BROWSER.find_element(By.NAME, "ctl00$cpExclusions$txtSBName").get_attribute("value")
                    if entity_field != entity:
                        self.get_entities_page()
                        continue
                    
                    # Find and press the search button
                    self.click_when_clickable("ctl00$cpExclusions$ibSearchSP", By.NAME)

                    # Check if next page loaded
                    next_page = self.check_exists("SP", By.ID)
                    if (not next_page):
                        self.get_entities_page()
                        continue
                    
                    # Check if results were found for the entity or not
                    check = self.check_exists("ctl00_cpExclusions_pnlEmpty", By.ID)
                    
                    # Check if folder exists for screenshots and create it if needed
                    if (os.path.exists("screenshots_entities/") == False):
                        os.makedirs("screenshots_entities")
                    
                    # Create screenshot path
                    path_screenshot = f"screenshots_entities/{str(entity)} OIG {str(month)} {str(year)}"
                    path_screenshot = path_screenshot.strip()
                    if not check:
                        path_screenshot += " CHECK"
                    path_screenshot += ".png"

                    # Find unique screenshot path and make a screenshot
                    unique_path_screenshot = self.find_unique_path_screenshot(path_screenshot)
                    self.take_screenshot("content", By.ID, unique_path_screenshot)
                    
                    # Return to the search page
                    self.back()

                    # Exit the loop
                    break

                except Exception as e:
                    print("-------------------------EXCEPTION OCCURED-----------------------------")
                    print(str(e))
                    print("---------------------------TRYING AGAIN--------------------------------")
                    try:
                        self.quit()
                    except NoSuchWindowException:
                        pass
                    self.create_browser()

            else:
                log_entry = f"Failed for - {entity}\n"
                print(log_entry)
                self.create_log_entry(log_entry)


        # Take a screenshot of either an entitiy or an individual
        data_len = len(data)
        if data_len == 1:
            entity = data.iloc[0]
            entity_take_screenshot(entity)
        elif data_len == 2:
            last_name = data.iloc[0]
            first_name = data.iloc[1]
            individual_take_screenshot(last_name, first_name)