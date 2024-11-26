from setuptools import setup

setup (
    name = 'package-name',
    version = 'version number: 0.0.0',
    description = 'A short description',
    long_description = 'file: README.rst',
    author = 'Author name',
    author_email = 'Optional: author e-mail',
    URL = 'https://www.github.com/',
    readme = 'README.rst',
    python_requires='>=3.7',
    classifiers= [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Customer Service',
        'License :: Free To Use But Restricted',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Communications :: Email'  
    ],
    package_dir ='src',
    include_package_data = True,
    install_requires = [
        'requirment1',
        'requirment2' 
        ]
        )