import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvacas-serlopal",
    version="0.1",
    author="Serlopal",
    author_email="oro_sergio@hotmail.com",
    description="scrapper that provides easy access to all Spanish holidays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Serlopal/pyvacas",
    packages=["pyvacas"], #setuptools.find_packages(),
    package_data={"cache": ["endpoint.pkl", "holidays.pkl", "locations.pkl"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
