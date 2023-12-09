=================
OIG Scanner
=================

-------------------------
Description
-------------------------
A package to automate checking and taking screenshots from Exclusions Database | Office of Inspector General ("https://exclusions.oig.hhs.gov/")

-------------------------
What it does
-------------------------
Given the data with either **entities (companies)** or **individuals (people)** in the format "<**last name**> <**first name**> or <**entity/company name**>,
finds them in Exclusions Database and takes a screenshot in the format "<**last name**> <**first name**> OIG <**month**> <**year**>.png" or
"<**entity/company name**> OIG <**month**> <**year**>.png". Appends the word "**CHECK**" to the end of a filename if the record is found, so the compliance
person later can verify if the given individual or entity works with them.

-------------------------
Installation and Usage
-------------------------
Run "pip install ." in the folder with "setup.py". If running using scripts or distribution, then install **firefox portable**
and **geckodriver**. Put them in the same folder with scripts. Then run the script with **xlsx** or **xls** file for data as a command-line argument.
If using distribution **exe** file, then can just drag and drop data file into the **exe** file.

-------------------------
Features
-------------------------
- can use multiple browsers and webdrivers (needs to be implemented in templates.py)
- can use different month and year if needed
- can use multiple threads (amount of cpu cores)
