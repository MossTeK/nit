from setuptools import setup, find_packages

setup(
    name='nit',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nit=nit.__main__:main',
        ],
    },
    install_requires=[
        'requests',
    ],
    python_requires='>=3.11',
    author='MossTeK',
    description='A small example package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
    
    url='https://github.com/MossTeK/nit',
)