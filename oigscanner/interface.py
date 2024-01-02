import numpy as np
import pandas as pd
import threading

from selenium.webdriver.remote.webdriver import WebDriver
from oigscanner.browser.handlers import oig_scanner
from oigscanner.browser import templates
from datetime import datetime
from typing import Callable


def interface(
    browser_template: Callable[[], WebDriver],
    data: pd.DataFrame,
    month: str = datetime.now().strftime("%B"),
    year: int = datetime.now().year,
    number_threads: int = 1
    ) -> None:
    """Runs OIG scans with given the number of threads, data, month, year, browser template

    Args:
        browser_template: function that will return a browser instance
        data: pandas dataframe with either one column (enitties) or two columns (individuals)
        month: month to append to the name of the screenshot
        year: year to append to the name of the screenshot
        number_threads: number of threads to use in doing oig scans
    """

    def take_oig(data_chunk: pd.DataFrame) -> None:
        """Helper function that creates instance of oig scanner and takes a screenshot with given data"""
        oig = oig_scanner(browser_template)
        data_chunk.apply(oig.take_oig_screenshot, args=(month,year), axis=1)


    # Split the data into given number of chunks
    data_chunks = np.array_split(data, number_threads)
    print("-------------------------------DATA----------------------------------")
    print(data)
    print("-------------------------SPLIT FOR THREARDS--------------------------")
    print(data_chunks)

    # Make threads on each chunk
    working_threads = []
    for i in range(number_threads):
        working_threads.append(threading.Thread(target=take_oig, args=(data_chunks[i],)))

    # Start threads
    for working_thread in working_threads:
        working_thread.start()

    # Join thread
    for working_thread in working_threads:
        working_thread.join()