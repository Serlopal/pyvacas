import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyVacas",
    version="v0.1.3-alpha",
    author="Serlopal",
    author_email="oro_sergio@hotmail.com",
    description="scrapper that provides easy access to all Spanish holidays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Serlopal/pyvacas",
    packages=["pyvacas"], #setuptools.find_packages(),
    package_data={"pyvacas/cache": ["endpoint.pkl", "holidays.pkl", "locations.pkl"]},
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'pandas',
       'beautifulsoup4',
       'requests-html'],
    setup_requires=[
        'pandas',
        'beautifulsoup4',
        'requests-html'],
    python_requires='>=3.5',
)
