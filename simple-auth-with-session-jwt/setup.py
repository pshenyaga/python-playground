from setuptools import setup
setup(
    name='auth-with-session-and-jwt',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=['auth_main', 'auth_protected'],
    install_requires=[
        'aiohttp',
        'aiohttp_session',
        'aiohttp_jinja2',
        'cryptography'],
    extras_require={
        'dev': ['gunicorn']
    }
)
