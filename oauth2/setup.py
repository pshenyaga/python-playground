from setuptools import setup, find_packages
setup(
    name="oauth2",
    version="0.1",
    package_dir={"": "src"},
    packages=["oauth2srv"],
    install_requires=['aiohttp'],
    extras_require={
        'dev': [ ]
    }
)
