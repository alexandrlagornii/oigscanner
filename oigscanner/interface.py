from oigscanner.browser.handlers import oig_scanner
from datetime import datetime
import numpy as np
import threading
import os

# Interface
def interface(browser_template, data,
              month=datetime.now().strftime("%B"), year=datetime.now().year,
              log_file_name="OIG_LOGS.txt", tries=5,
              multiple_threads=False):

    # Helper function to do OIG for individuals
    def do_individuals_oig(data):
    
        # Create browser
        browser = oig_scanner(browser_template())

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
                    browser = oig_scanner(browser_template())
                else:
                    break
            
            # If failed create entry in the log
            else:
                with open(log_file_name, "a+", encoding="utf-8") as log:
                    log.write(f"Failed for - {last_name} {first_name}\n")

    # Helper function to do OIG for entities
    def do_entities_oig(data):

        # Create browser
        browser = oig_scanner(browser_template())

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
                    browser = oig_scanner(browser_template())
                else:
                    break

            # If failed create entry in the log
            else:
                with open(log_file_name, "a+", encoding="utf-8") as log:
                    log.write(f"Failed for - {entity}\n")

    # Helper function for running one thread
    def one_thread_oig_scans():

        # Check if OIG needed for individuals or entities
        columns = len(data.columns)

        # If one column => OIG scans for entities
        if columns == 1:
            do_entities_oig(data)

        # If two columns => OIG scans for individuals
        elif columns == 2:
            do_individuals_oig(data)

    # Helper function for running multiple threads
    def multiple_threads_oig_scans():
        
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