from setuptools import setup
import setuptools

# get __version__, __author__, and __email__
exec(open("./couzinswarm/metadata.py").read())

setup(name='couzinswarm',
      version=__version__,
      description="Simulating fish swarming behavior with the model by Iain Couzin et al.",
      url='https://www.github.com/benmaier/couzinswarm',
      author=__author__,
      author_email=__email__,
      license=__license__,
      packages=setuptools.find_packages(),
      install_requires=[
          'numpy>=1.14',
          'progressbar2',
      ],
      zip_safe=False)
