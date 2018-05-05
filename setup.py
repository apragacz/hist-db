import os.path
import re
from setuptools import setup, find_packages


ROOT_DIR = os.path.dirname(__file__)


def read_contents(local_filepath):
    with open(os.path.join(ROOT_DIR, local_filepath)) as f:
        return f.read()


def get_requirements(requirements_filepath):
    '''
    Return list of this package requirements via local filepath.
    '''
    return read_contents(requirements_filepath).split('\n')


def get_version(package):
    '''
    Return package version as listed in `__version__` in `init.py`.
    '''
    init_py = read_contents(os.path.join(package, '__init__.py'))
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description(markdown_filepath):
    '''
    Return the long description in RST format, when possible.
    '''
    try:
        import pypandoc
        return pypandoc.convert(markdown_filepath, 'rst')
    except ImportError:
        return read_contents(markdown_filepath)


setup(
    name='hist-db',
    version=get_version('hist_db'),
    packages=find_packages(exclude=['tests.*', 'tests']),
    author='Andrzej Pragacz',
    author_email='apragacz@o2.pl',
    description=(
        'Util enhancing reverse-i-search in shell'
    ),
    license='MIT',
    keywords=' '.join((
        'bash',
        'sh',
        'shell',
        'history',
        'histfind',
        'hist-db',
        'hist-find',
        'hist',
        'reverse',
        'search',
        'reverse-i-search',
        'find',
    )),
    long_description=get_long_description('README.md'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    install_requires=get_requirements('requirements.txt'),
    url='https://github.com/apragacz/hist-db',
    entry_points={
        'console_scripts': [
            'hist-db = hist_db.main:main',
        ],
    },
)
