from setuptools import setup, find_packages

setup(
    name='sdltm2tmx',
    version='0.1',
    description='convert sdltm translation memories to tmx1.4',
    author='Gregory Vigo Torres',
    license='gplv3',
    classifiers=[
        'Development Status :: 4 Beta',
        'Programming Language :: Python :: 3'
    ],
    keywords='translation localization',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sdltm2tmx-cli=sdltm2tmx:main'
        ],
    },
)
