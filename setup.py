from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="sentiment-analyzer-app",
    version="1.0.0",
    author="Sentiment Analysis Team",
    author_email="support@sentimentanalyzer.com",
    description="AI-powered sentiment analysis web application with RoBERTa model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sentiment-analyzer/app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pyinstaller>=5.0", "pytest>=7.0"],
    },
    entry_points={
        "console_scripts": [
            "sentiment-analyzer=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "requirements.txt"],
    },
)
