"""
Setup script for the task manager application.
"""

from setuptools import setup, find_namespace_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements.txt if it exists, otherwise use minimal requirements
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
else:
    requirements = [
        "streamlit>=1.22.0",
        "pytest>=7.3.1"
    ]

setup(
    name="task-manager",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple task management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/task-manager",
    package_dir={"": "."},
    packages=find_namespace_packages(include=["src", "src.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "task-manager=src.cli:main",
        ],
    },
)
