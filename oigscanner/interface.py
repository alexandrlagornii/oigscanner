import numpy as np
import pandas as pd
import threading

from selenium.webdriver.remote.webdriver import WebDriver
from oigscanner.browser.handlers import oig_scanner
from oigscanner.browser import templates
from datetime import datetime

from typing import Union
from typing import Callable


def interface(
    browser_template: Callable[[], WebDriver],
    data: pd.DataFrame,
    month: str = datetime.now().strftime("%B"),
    year: int = datetime.now().year,
    log_file_name: str = "OIG_LOGS.txt",
    tries: int = 5,
    number_threads: int = 1
    ) -> None:
    """Does OIG scans

    Args:
        browser_template: function that will return a browser instance
        data: pandas dataframe with either one column (enitties) or two columns (individuals)
        month: month to append to the name of the screenshot
        year: year to append to the name of the screenshot
        log_file_name: name of the file for logs
        tries: in case of timeout or other exception tries to still take the screenshot for the given number
        multiple_threads: flag to show whether multiple instances of webdrivers will do the work
    """

    def create_browser() -> Union[oig_scanner]:
        """Helper function that will create oig scanner with an instance of a webdriver from a given template"""

        browser_instance = browser_template()
        browser = oig_scanner(browser_instance)
        return browser


    def do_individuals_oig(data: pd.DataFrame) -> None:
        """Helper function to do OIG for individuals

        Args:
            data: pandas dataframe with either entities or individuals
        """
    
        # Create browser
        browser = create_browser()

        # Iterate over each individual
        for index, row in data.iterrows():

            # Get last name and first name from the list
            last_name = row.iloc[0]
            first_name = row.iloc[1]

            # Try to get a screenshot, if error try again
            for i in range(tries):
                try:
                    browser.individual_take_screenshot(last_name, first_name, month, year)
                except Exception as e:
                    print(str(e))
                    browser = create_browser()
                else:
                    break
            
            # If failed create entry in the log
            else:
                with open(log_file_name, "a+", encoding="utf-8") as log:
                    log.write(f"Failed for - {last_name} {first_name}\n")


    def do_entities_oig(data: pd.DataFrame) -> None:
        """Helper function to do OIG for entities

        Args:
            data: pandas dataframe with either entities or individuals
        """

        # Create browser
        browser = create_browser()

        # Iterate over each company
        for index, row in data.iterrows():

            # Get entity
            entity = row.iloc[0]

            # Try to get a screenshot, if error try again
            for i in range(tries):
                try:
                    browser.entity_take_screenshot(entity, month, year)
                except Exception as e:
                    print(str(e))
                    browser = create_browser()
                else:
                    break

            # If failed create entry in the log
            else:
                with open(log_file_name, "a+", encoding="utf-8") as log:
                    log.write(f"Failed for - {entity}\n")


    def run_oig_scans() -> None:
        """Runs oig with given number of threads"""
        
        # Split the data into given number of chunks
        data_chunks = np.array_split(data, number_threads)
        print(data_chunks)

        # Check if OIG needed for individuals or entities
        columns = len(data.columns)

        # Get the right function
        if columns == 1:
            thread_function = do_entities_oig
        elif columns == 2:
            thread_function = do_individuals_oig

        # Make threads on each chunk
        working_threads = []
        for i in range(number_threads):
            working_threads.append(threading.Thread(target=thread_function, args=(data_chunks[i],)))

        # Start threads
        for working_thread in working_threads:
            working_thread.start()

        # Join thread
        for working_thread in working_threads:
            working_thread.join()


    # Set log start
    with open(log_file_name, "a+", encoding="utf-8") as log:
        log.write(f"START at {datetime.now()}\n")

    # Run the scanner with given number of threads
    run_oig_scans()

    # End log and finish
    with open(log_file_name, "a+", encoding="utf-8") as log:
        log.write(f"END at - {datetime.now()}\n")