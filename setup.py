from setuptools import find_packages, setup

# Read the contents of README.md for the long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linkup-sdk",
    version="0.1.7",
    author="LINKUP TECHNOLOGIES",
    author_email="contact@linkup.so",
    description="A Python Client SDK for the Linkup API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LinkupPlatform/linkup-python-sdk",
    project_urls={
        "Documentation": "https://github.com/LinkupPlatform/linkup-python-sdk#readme",
        "Source Code": "https://github.com/LinkupPlatform/linkup-python-sdk",
        "Issue Tracker": "https://github.com/LinkupPlatform/linkup-python-sdk/issues",
    },
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="linkup api sdk client search",
    packages=find_packages(),
    package_data={"linkup": ["py.typed"]},
    python_requires=">=3.8",
    install_requires=[
        "httpx",
        "pydantic",
    ],
)
