from setuptools import setup, find_packages

setup(
    name="arkham-ctf",
    version="1.0.0",
    description="ARKHAM - Automated Reconnaissance & Knowledge HARvesting Agent of Providence",
    author="rhizor",
    author_email="rhizor@example.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "arkham=arkham.cli:main",
            "arkham-agent=arkham.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
    ],
)
