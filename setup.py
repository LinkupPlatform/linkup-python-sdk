from typing import Optional

from setuptools import find_packages, setup

# Read the content of linkup/_version.py for the version, without importing the module
# This assumes the version is defined as `__version__ = "x.y.z"` (support type hint or inline
# comment at the end of the line)
version: Optional[str] = None
with open("linkup/_version.py", "r") as version_file:
    for line in version_file.readlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].split("#")[0].strip().strip('"').strip("'")
            break
if version is None:
    raise ValueError("Could not determine the version from linkup/_version.py")


# Read the content of README.md for the long description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


setup(
    name="linkup-sdk",
    version=version,
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
    python_requires=">=3.9",
    install_requires=[
        "httpx",
        "pydantic",
    ],
)
