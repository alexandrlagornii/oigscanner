import os
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class browser_wrapper:

    def __init__(
        self,
        browser: webdriver.WEBDRIVER,
        wait_time: int = 10,
        timeout: int = 20
        ):
        """Set reference to an instance of a webdriver. Set time to wait for html element. Set timout.

        Args:
            browser: instance of webdriver
            wait_time: time to wait for an element to be found
            timout: time to wait if nothing is happening
        """

        # Set browser
        self.BROWSER = browser

        # Set wait time
        self.WAIT = WebDriverWait(self.BROWSER, wait_time)

        # Set timout time
        self.BROWSER.set_page_load_timeout(timeout)


    def __del__(self):
        """Closes webdriver instance"""
        self.BROWSER.quit()
        

    def check_exists(
        self,
        element_name: str,
        attribute: By.ATTRIBUTE
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
            return True
        except NoSuchElementException:
            return False


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


    def find_unique_path_screenshot(self, path_screenshot: str) -> bool:
        """Checks if there is a screenshot with the same name and adds number to the name if there is.
        
        Args:
            path_screenshot: path of a screenshot

        Returns:
            Unique screenshot path if found, False if not
        """

        # Search for duplicates
        for i in range(1, 1_000_000_000):

            if (os.path.isfile(path_screenshot)):

                # Remove file format
                path_screenshot = path_screenshot.removesuffix(".png")

                # Remove brackets with numbers
                pattern = r"\(\d*?\)"
                path_screenshot = re.sub(pattern, "", path_screenshot)

                # Remove white space
                path_screenshot = path_screenshot.strip()
                
                # Make new name
                path_screenshot += " (" + str(i) + ")"
                path_screenshot += ".png"
        
            else:
                return path_screenshot
        
        # If couldn't get unique name
        else:
            return False


    def get(self, page: str) -> None:
        """Given page open it with the browser
        
        Args:
            page: URL of the page
        """
        self.BROWSER.get(page)


    def back(self) -> None:
        "Go back to the previous page"
        self.BROWSER.back()


    def quit(self) -> None:
        "Close browser thus quitting webdriver"
        self.BROWSER.quit()


class oig_scanner(browser_wrapper):

    # Initialize
    def __init__(self, browser, wait_time=10, timeout=20, try_page=5):
        """Opens the browser and gets the oig exclusions site"""

        # Open browser
        super().__init__(browser, wait_time, timeout)

        # Set up constants
        self.TRY_PAGE = try_page

        # Get the main website
        self.get("https://exclusions.oig.hhs.gov")

    # Helper function to get back to the main page for individuals
    def get_individuals_page(self):
        """Gets first page of oig exclusions site"""
        self.get("https://exclusions.oig.hhs.gov")

    # Helper function to get back to the main page for entities
    def get_entities_page(self):
        """Gets first page of oig exclusions site and sets searching for entities"""
        self.get("https://exclusions.oig.hhs.gov")
        self.click_when_clickable("ctl00_cpExclusions_Linkbutton1", By.ID)
        
    # Take a screenshot for an individual
    def individual_take_screenshot(self, last_name, first_name, month, year):
        """Takes a screenshot of an individual last name and first name"""

        # Print person
        print(f"{last_name} , {first_name}")

        # If something wrong try again
        for i in range(self.TRY_PAGE):

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

            # Check if there is a duplicate and make a copy with number indicating its appearance
            path_screenshot = self.find_unique_path_screenshot(path_screenshot)
            
            # Take a screenshot
            self.take_screenshot("content", By.ID, path_screenshot)
            
            # Return to the search page
            self.back()

            # Return True if everything is okay
            return True

        # Otherwise False
        else:
            return False

    # Take a screenshot for an individual
    def entity_take_screenshot(self, entity, month, year):
        """Takes a screenshot of an entity given its name"""

        # Print entity
        print(entity)

        # If something wrong try again
        for i in range(self.TRY_PAGE):

            # Check if page loaded correctly
            exists_entity = self.check_exists("ctl00$cpExclusions$txtSBName", By.NAME)
            if not exists_entity:
                self.get_entities_page()
                continue

            # Entity name
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

            # Check if there is a duplicate and make a copy with number indicating its appearance
            path_screenshot = self.find_unique_path_screenshot(path_screenshot)

            # Take a screenshot
            self.take_screenshot("content", By.ID, path_screenshot)

            # Return to the search page
            self.back()

            # Return True if everything is okay
            return True

        # Otherwise False
        else:
            return False