import numpy as np
import pandas as pd
import threading
import os

from oigscanner.browser.handlers import oig_scanner
from oigscanner.browser import templates
from datetime import datetime


# Interface
def interface(
    browser_template: templates,
    data: pd.DataFrame,
    month: str = datetime.now().strftime("%B"),
    year: int = datetime.now().year,
    log_file_name: str = "OIG_LOGS.txt",
    tries: int = 5,
    multiple_threads: bool = False
    ) -> None:
    """Does OIG scans

    Args:
        browser_template: function that will return a browser instance
        data: pandas dataframe with either one column (enitties) or two columns (individuals)
        month: month to append to the name of the screenshot
        year: year to append to the name of the screenshot
        log_file_name: name of the file for logs
        tries: in case of timeout or other exception tries to still take the screenshot for the given amount
        multiple_threads: flag to show whether multiple instances of webdrivers will do the work
    """

    def do_individuals_oig(data: pd.DataFrame) -> None:
        """Helper function to do OIG for individuals

        Args:
            data: pandas dataframe with either entities or individuals
        """
    
        # Create browser
        try:
            browser_instance = browser_template()
            browser = oig_scanner(browser_instance)
        except Exception as e:
            print(str(e))

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
                    browser_instance = browser_template()
                    browser = oig_scanner(browser_instance)
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
        try:
            browser_instance = browser_template()
            browser = oig_scanner(browser_instance)
        except Exception as e:
            print(str(e))

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
                    browser_instance = browser_template()
                    browser = oig_scanner(browser_instance)
                else:
                    break

            # If failed create entry in the log
            else:
                with open(log_file_name, "a+", encoding="utf-8") as log:
                    log.write(f"Failed for - {entity}\n")


    def one_thread_oig_scans() -> None:
        """Runs OIG scans on one thread"""

        # Check if OIG needed for individuals or entities
        columns = len(data.columns)

        # If one column => OIG scans for entities
        if columns == 1:
            do_entities_oig(data)

        # If two columns => OIG scans for individuals
        elif columns == 2:
            do_individuals_oig(data)


    def multiple_threads_oig_scans() -> None:
        """Runs oig on amount of CPU cores threads"""
        
        # Get amount of threads
        amount_threads = os.cpu_count()

        # Split the data into given amount of chunks
        data_chunks = np.array_split(data, amount_threads)
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
        for i in range(amount_threads):
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

    # Run the scanner with given amount of threads
    if (multiple_threads):
        multiple_threads_oig_scans()
    else:
        one_thread_oig_scans()

    # End log and finish
    with open(log_file_name, "a+", encoding="utf-8") as log:
        log.write(f"END at - {datetime.now()}\n")