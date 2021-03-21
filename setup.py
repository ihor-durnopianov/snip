# -*- coding: utf-8 -*-
""""""


from setuptools import setup


setup(
    name='snip',  # Required

    version='0.0.1',  # Required

    description='Tool to help with snippets',  # Optional

    py_modules=["snip"],  # Required

    python_requires='>=3.6',

    install_requires=[],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'snip=snip:main',
        ],
    },
)
