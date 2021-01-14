from distutils.core import setup
from ezcliy import __version__

setup(
    name='ezcliy',
    version=__version__,
    packages=['ezcliy'],
    url='https://github.com/kpostekk/ezcliy',
    license='Apache License',
    author='Krystian Postek',
    author_email='krystian@postek.eu',
    description='Framework for creating CLI tools'
)
