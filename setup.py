from setuptools import setup, find_packages

setup(
    name="earth2mars-ai",
    version="0.1.0",
    author="Muhammad Zeeshan",
    description="Earth2Mars AI: Intelligent Earth Analog Discovery for Moon and Mars Exploration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MalikZeeshan1122/earth2mars-ai",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "rasterio>=1.3.0",
        "geopandas>=0.13.0",
        "streamlit>=1.28.0",
        "plotly>=5.18.0",
        "torch>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="nasa moon mars analog geospatial machine-learning satellite",
)
