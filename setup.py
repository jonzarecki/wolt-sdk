#!/usr/bin/env python3
"""
Setup script for Wolt Restaurant Availability API
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wolt-api",
    version="0.1.0",
    author="Wolt API Contributors",
    description="Python API for checking restaurant availability on Wolt in Israel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/wolt-access",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/wolt-access/issues",
        "Documentation": "https://github.com/your-username/wolt-access#readme",
        "Source Code": "https://github.com/your-username/wolt-access",
        "Changelog": "https://github.com/your-username/wolt-access/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Financial",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
        ],
    },
)