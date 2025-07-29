from setuptools import setup, find_packages

setup(
    name="crypto-momentum-analyzer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.9.1",
        "pandas==2.1.4", 
        "numpy==1.26.2",
        "ta==0.10.2",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "tqdm==4.66.1"
    ],
    author="Abhinav V",
    description="cryptocurrency momentum analysis system",
    python_requires=">=3.8",
)