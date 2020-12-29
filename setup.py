import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anserializer",
    version="1.0.0",
    author="anttin",
    author_email="muut.py@antion.fi",
    description="A serializer/deserializer mechanism for simple and complex data structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anttin/anserializer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
