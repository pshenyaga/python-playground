from setuptools import setup, find_packages
setup(
    name='jwt_playground',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=['jwtprotected'],
    install_requires=['aiohttp', 'PyJWT'],
    extras_require={
        'dev': ['gunicorn', 'httpie']
    }
)
