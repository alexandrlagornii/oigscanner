from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import re

# Browser wrapper
class browser_wrapper:

    # Initialize
    def __init__(self, browser, wait_time=10, timeout=20):
        """Set BROWSER and WAIT constant"""

        # Set browser
        self.BROWSER = browser

        # Set wait time
        self.WAIT = WebDriverWait(self.BROWSER, wait_time)

        # Set timout time
        self.BROWSER.set_page_load_timeout(timeout)

    # Destructor
    def __del__(self):
        self.BROWSER.quit()
        
    # Check if element exists
    def check_exists(self, element_name, attribute):
        """Check if element exists and return true if it does, otherwise false"""
        
        try:
            self.BROWSER.find_element(attribute, element_name)
        except NoSuchElementException:
            return False
        return True
    
    # Enter value
    def enter_value(self, element_name, attribute, value):
        """Enter value into the field given element and its attribute"""

        # Find and wait until it's clickable
        element = self.WAIT.until(EC.element_to_be_clickable((attribute, element_name)))
        
        # Enter the value
        element.click()
        element.clear()
        element.send_keys(value)

    # Wait until is clickable and then clicking
    def click_when_clickable(self, element_name, attribute):
        """Click on an element when possible with given attribute"""

        # Find
        element = self.WAIT.until(EC.element_to_be_clickable((attribute, element_name)))
    
        # Click
        element.click()
    
    # Take a screenshot of an element
    def take_screenshot(self, element_name, attribute, path_screenshot):
        """Takes a screenshot of an element given element name, attribute, and a path to the screenshot"""

        # Find
        element = self.WAIT.until(EC.visibility_of_element_located((attribute, element_name)))   

        # Take a screenshot
        element.screenshot(path_screenshot)

    # Find a unique path for a screenshot
    def find_unique_path_screenshot(self, path_screenshot):
        """Checks if there is a screenshot with the same name and adds number to the name if there is"""

        # Search for duplicates
        for i in range(1, 1_000_000_000):
            if (os.path.isfile(path_screenshot)):
                # Remove file format
                path_screenshot = path_screenshot.removesuffix(".png")

                # Remove brackets with numbers
                pattern = "\(\d*?\)"
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

    # Get page
    def get(self, page):
        "Given page open it with the browser"
        self.BROWSER.get(page)

    # Get previous page
    def back(self):
        "Go back to the previous page"
        self.BROWSER.back()

    # Quit webdriver
    def quit(self):
        "Close browser thus quitting webdriver"
        self.BROWSER.quit()

# OIG Scanner
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