from setuptools import setup, find_packages
from opensbt.version import __version__
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='opensbt',
    version=__version__,
    packages=find_packages(include=['opensbt', 'opensbt.*']),
    include_package_data=True,
    exclude_package_data={
        '': ['*.pyc', 
             'opensbt/results/*'
             '*.pyx',
             '*/*log.txt',
             '*/results/*'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    description="OpenSBT is a Modular Framework for Search-based Testing of Automated Driving Systems",
    author="Lev Sorokin",
    author_email="sorokin@fortiss.org",
    license="Apache",
    classifiers=[
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: POSIX :: Linux"
    ],
    install_requires=[
        'deap==1.4.1',
        'numpy==1.24.4',
        'scipy==1.10.1',
        'matplotlib==3.7.4',
        'pandas==2.0.3',
        'setuptools',
        'scikit-learn==1.3.2',
        'pymoo==0.6.0.1'
    ],
    python_requires=">=3.8"
)
