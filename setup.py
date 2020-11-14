import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotics_pkg",
    version="0.0.1",
    author="Gabriel Almeida Borges",
    author_email="gabrielborges031807@gmail.com",
    packages=["robotics_pkg"],
    description="A small package for robotics and transform matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GB0307/robotics_package",
    license='GPT',
    python_requires='>=3.5',
    install_requires=[
         "numpy>=1.17.4",
    ]
)