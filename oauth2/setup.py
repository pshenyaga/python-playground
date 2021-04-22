from setuptools import setup, find_packages
setup(
    name='oauth2',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=[
        'oauth2helpers',
        'oauth2srv',
        'oauth2srv.models'
        'oauth2client',
        'oauth2protected'],
    install_requires=['aiohttp', 'aiohttp_jinja2', 'webargs'],
    extras_require={
        'dev': [ ]
    }
)
