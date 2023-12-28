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
Installation
-------------------------
1. Run "pip install -r requirements.txt"
2. Run "pip install ." in the folder with "setup.py".
3. Install **firefox portable** and **geckodriver**, then put them in the same folder with scripts. (If using scripts in the repository)

-------------------------
Usage
-------------------------
The entry point are python scripts in the scripts folder. Provided you installed everything correctly, the folder should look like this
.. image:: ../docs/img/layout.png
    :alt: Layout of Folder


-------------------------
Features
-------------------------
- can use multiple browsers and webdrivers (needs to be implemented in templates.py)
- can use different month and year if needed
- can use multiple threads
