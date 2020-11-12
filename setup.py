import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotics_pkg",
    version="0.0.1",
    author="Gabriel Almeida Borges",
    author_email="reza@cpol.co",
    packages=["robotics_pkg"],
    description="A small package for robotics and transform matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/example-pkg",
    license='GPT',
    python_requires='>=3.4',
    install_requires=[
         "numpy>=1.17.4",
    ]
)