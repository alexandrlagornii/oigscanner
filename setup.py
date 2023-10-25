from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'OIG scanner'
LONG_DESCRIPTION = 'OIG scanner'

# Setting up
setup(
        name="oigscanner", 
        version=VERSION,
        author="Alexandr Lagornii",
        author_email="alexandrlagornii@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'oigscanner'],
        classifiers= [
            "Intended Audience :: Enterprise",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)