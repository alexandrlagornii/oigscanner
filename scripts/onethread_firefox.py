import pandas as pd
import sys

from oigscanner.browser.templates import firefox_template
from oigscanner.data.processing import normalize_data_oig
from oigscanner.interface import interface


try:
    # Set paths
    path_binary = "FirefoxPortable/App/Firefox64/firefox.exe"
    path_driver = "geckodriver.exe"

    # Get data
    data_path = str(sys.argv[1])
    data = pd.read_excel(data_path)
    data = normalize_data_oig(data)

    # Run scanner with given template
    browser_template = firefox_template(path_binary, path_driver)
    interface(browser_template, data)

except Exception as e:
    print(str(e))
    sys.exit(1)