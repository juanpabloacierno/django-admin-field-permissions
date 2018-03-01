import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'readme.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dafpermission',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='A simple Django app to create profiles of field based permissions including hide, read-only and read & write.',
    long_description=README,
    url='https://github.com/ezenechea/dafpermission',
    author=['Ismael Bejarano','Ezequiel Aurtenechea','Ezequiel Cascardo'],
    author_email='mail@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
