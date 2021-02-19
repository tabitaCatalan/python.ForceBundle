# setup.py
from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='forcebundle', 
    version='0.0.1',
    description="Implementation of Force-directed Edge Bungling for Graph Visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tabitaCatalan/python.ForceBundle", 
    author="Vera Sativa",
    author_email="hola@verasativa.com", 
    maintainer="Tabita Catalán",
    maintainer_email="tcatalan@dim.uchile.cl",
    #package_dir={"": "src"},
    packages=find_packages(),
    install_requires=[
        'numba>=0.4',
        'tqdm>=2'
    ],
    extras_require={
        "dev": [
            "pytest>=6.0", 
            "bump2version>=1.0"
        ], 
        "plots":[
            "matplotlib >= 3.0", 
            "numpy >= 1.2", 
            "notebook >= 6.0"
        ]
    }, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
