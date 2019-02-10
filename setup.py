from setuptools import setup

setup(
    name='PennPy',
    packages=['PennPy'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_bootstrap',
        'flask_nav',
        'flask-mysqldb',
        'flask-WTF',
        'passlib',

    ],
)
