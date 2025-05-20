"""
Setup script for the task manager application.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Core package dependencies
install_requires = [
    "streamlit>=1.22.0",
]

# Test dependencies
tests_require = [
    "pytest>=7.3.1",
    "pytest-cov>=4.1.0",
    "flake8>=6.0.0",
]

# Development dependencies
extras_require = {
    "dev": tests_require + [
        "build>=1.0.0",
        "wheel>=0.40.0",
    ]
}

setup(
    name="task-manager",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple task management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/task-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "task-manager=src.cli:main",
        ],
    },
)
