from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='locdata',
   version='0.1',
   description='',
   license="agpl-3.0",
   long_description=long_description,
   author='Daniel Marasco',
   author_email='',
   url="",
   packages=find_packages(where='src'),
   package_dir={'': 'src'},
   install_requires=[], #external packages as dependencies
   scripts=[
           ]
)