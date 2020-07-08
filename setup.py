import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvacas",
    version="0.0.1",
    author="Serlopal",
    author_email="oro_sergio@hotmail.com",
    description="scrapper that provides easy access to all Spanish holidays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Serlopal/pyvacas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)