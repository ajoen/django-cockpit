import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cockpit',
    version='0.1',
    packages=['cockpit'],
    include_package_data=True,
    long_description=README,
    url='https://github.com/ajoen/django-cockpit/',
    license='Apache License, Version 2.0',
    author='Berker Sonmez',
    author_email='brkrsnmz@gmail.com',
    description='Dead simple CMS for django 1.5+',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License, Version 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
