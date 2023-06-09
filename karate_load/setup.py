from setuptools import setup, find_packages

setup(
    name='karate_loader',
    version='0.1',
    packages=find_packages(),
    install_requires=['GraphIt>=0.1'],
    entry_points={
        'data.load':
            ['karate_load=karate_load.karate_load:KarateLoader']
    },
    zip_safe=True
)