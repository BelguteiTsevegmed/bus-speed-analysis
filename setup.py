from setuptools import setup, find_packages

setup(
    name='package',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas~=2.0.3',
        'requests~=2.31.0',
        'numpy~=1.24.4',
        'matplotlib~=3.7.5',
        'setuptools~=67.8.0',
        'scikit-learn~=1.3.2'
    ]
)
