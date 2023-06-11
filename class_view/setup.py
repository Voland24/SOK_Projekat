from setuptools import setup, find_packages

setup(
    name='class_view_loader',
    version='0.1',
    packages=find_packages(),
    install_requires=['GraphIt>=0.1'],
    entry_points={
        'data.display':
            ['class_view_loader=class_view.class_view:ClassViewLoader']
    },
    package_data={'class_view_loader': ['static/*.css', 'static/*.js', 'static/*.html', 'scripts/*.js']},
    zip_safe=True
)
