from setuptools import setup, find_packages

setup(
    name='GraphIt',
    version='0.1',
    packages=find_packages(),
    install_requires=['Django>=2.1'],

    package_data={'GraphIt': ['templates/*.html', 'static/*.css', 'static/*.js', 'static/*.html', 'scripts/*.html']},
    zip_safe=True,
)
