import os
from setuptools import setup


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
    url='https://github.com/yourname/django-myapp/',
    license='MIT',
    install_requires=[
        'Django=4.0.1',
    ]
)