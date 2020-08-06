from setuptools import setup, find_packages


VERSION = '2.0'

setup(
    name='sdltm2tmx',
    version=VERSION,
    description='convert sdltm translation memories to tmx1.4',
    author='Gregory Vigo Torres',
    license='gplv3',
    classifiers=[
        'Development Status :: 4 Beta',
        'Programming Language :: Python :: 3'
    ],
    keywords='translation localization',
    packages=find_packages(),
    install_requires=[
        'click',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'sdltm2tmx=sdltm2tmx.sdltm2tmx_cli:main'
        ],
    },
)
