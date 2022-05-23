import os
from setuptools import setup

#pip install git+https://github.com/deepakkumhar/deepakpackagee/#egg=social
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='social',
    version='0.1',
    packages=['social'],
    description='A line of description',
    long_description=README,
    author='deepak',
    author_email='yourname@example.com',
    url='https://github.com/deepakkumhar/deepakpackagee/social=0.1',
    license='MIT',

)
