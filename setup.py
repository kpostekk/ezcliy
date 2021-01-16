from distutils.core import setup
from ezcliy import __version__


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    install_requires=["colorama==0.4.4", "pyyaml==5.3.1"],
    name="ezcliy",
    version=__version__,
    packages=["ezcliy"],
    url="https://github.com/kpostekk/ezcliy",
    license="Apache",
    author="Krystian Postek",
    author_email="krystian@postek.eu",
    description="Framework for creating CLI tools",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    long_description=readme()
)
