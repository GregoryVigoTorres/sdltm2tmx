from setuptools import setup, find_packages


setup(
    name='sdltm2tmx',
    version='1.0',
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
    dependency_links=[
        'git+https://gitlab.com/grgvt/tmx_writer.git#egg=tmx-writer-1.1',
    ],
    entry_points={
        'console_scripts': [
            'sdltm2tmx=sdltm2tmx.sdltm2tmx_cli:main'
        ],
    },
)
