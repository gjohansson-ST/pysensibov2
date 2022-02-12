"""A setuptools based setup module."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

print(find_packages())
setup(
    name='pysensibov2',
    version='1.0.0',
    description='Python API for Sensibo',
    long_description=long_description,
    url='https://github.com/gjohansson-ST/pysensibov2',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Sensibo',
    install_requires=['aiohttp'],
    zip_safe=True,
    author='gjohansson-ST',
    author_email='goran.johansson@shiftit.se',
    packages=find_packages()
)
