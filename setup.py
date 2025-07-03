"""
Setup script for the task manager application.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="task-manager",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple task management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/task-manager",
    packages=find_packages(include=["src", "src.*", "tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "task-manager=src.cli:main",
        ],
    },
)
