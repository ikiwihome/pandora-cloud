# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from src.pandora_cloud import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup(
    name='Pandora-Cloud',
    version=__version__,
    python_requires='>=3.7',
    author='ikiwi',
    author_email='ikiwicc@gmail.com',
    keywords='OpenAI ChatGPT ChatGPT-Plus',
    description='A true web for ChatGPT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ikiwihome/pandora',
    packages=find_packages('src'),
    package_dir={'pandora_cloud': 'src/pandora_cloud'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pandora = pandora_cloud.cloud_launcher:run',
        ]
    },
    project_urls={
        'Source': 'https://github.com/ikiwihome/pandora',
        'Tracker': 'https://github.com/ikiwihome/pandora/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Web Environment',

        'Framework :: Flask',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
