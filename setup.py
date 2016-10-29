from setuptools import setup

__version__ = '0.0.1a'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

extra_setuptools_args = dict(
    tests_require=['pytest']
    )

setup(
    name='samplesize',
    version=__version__,
    description='Sample size extraction for scientific writing',
    maintainer='Taylor Salo',
    maintainer_email='tsalo006@fiu.edu',
    install_requires=['nltk', 'pandas'],
    packages=['samplesize'],
    license='MIT',
    **extra_setuptools_args
)
