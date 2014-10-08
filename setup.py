try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
try:
    from setuptools import find_packages
except ImportError:
    from distutils.core import find_packages

packages = find_packages()

setup(
    name = "file-stalker",
    version = "0.0.2",
    author = "Francis Lavoie",
    author_email = "lav.francis@gmail.com",
    description = "Skalk a directory and run a command when something change",
    license ="MIT License",
    url = "git@github.com:francisl/file-stalker.git",
    scripts=['src/stalk.py'],
    packages = [
        "src"
    ],

    install_requires = []
)