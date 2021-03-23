from setuptools import setup, find_packages
setup(
    name='jwt_playground',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=['jwt_protected'],
    install_requires=['aiohttp', 'aiohttp_jinja2'],
    extras_require={
        'dev': [ ]
    }
)
