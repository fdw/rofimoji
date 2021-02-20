from setuptools import setup

setup(
    name='rofimoji',
    version='5.0.0',
    description='Simple character picker using rofi',
    author='fdw',
    author_email='5821180+fdw@users.noreply.github.com',
    url='https://github.com/fdw/rofimoji',
    keywords='rofi emoji emoji-picker picker emoticon smiley utf-8 character-picker',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],

    packages=['picker'],
    package_data={
        'picker': ['data/*.csv']
    },
    entry_points={
        'console_scripts': [
            'rofimoji = picker.rofimoji:main'
        ]
    },
    install_requires=[
        'ConfigArgParse>0.15,<2.0.0'
    ],
    data_files=[
        ('share/man/man1', ['picker/docs/rofimoji.1'])
    ]
)
