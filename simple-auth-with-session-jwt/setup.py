from setuptools import setup
setup(
    name='auth-with-session-and-jwt',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=['auth_main', 'auth_protected'],
    install_requires=['aiohttp'],
    extras_require={
        'dev': ['gunicorn']
    }
)
