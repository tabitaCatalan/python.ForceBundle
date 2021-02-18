# setup.py
from setuptools import setup

setup(
    name='forcebundle', 
    version='0.0.1',
    description='Say hello!',
    url="https://github.com/tabitaCatalan/python.ForceBundle", 
    author="Vera Sativa",
    author_email="hola@verasativa.com", 
    maintainer="Tabita Catalán",
    maintainer_email="tcatalan@dim.uchile.cl",
    py_modules=["ForcedirectedEdgeBundling"], 
    package_dir={"": "src"},
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
            "matplotlib", 
            "numpy"
        ]
    }, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
