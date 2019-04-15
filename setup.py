import os
from distutils.core import setup
from setuptools import find_packages

__version__ = open("piedpiper/version.py").readline().split(" = ")[1].replace(
    '"', '').strip()

install_requires = []

setup(
    name="piedpiper",
    packages=find_packages(),
    version=__version__,
    description="Debug context manager for chained commands.",
    author="Endre Bakken Stovner",
    author_email="endrebak85@gmail.com",
    url="http://github.com/endrebak/piedpiper",
    keywords=["Debugging"],
    license="MIT",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta", "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: MIT License',
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering"
    ],
    long_description=("Debug context manger for method chaining."))
