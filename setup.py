from setuptools import setup

setup(name='couzinswarm',
      version='0.0.1',
      description="Simulating fish swarming behavior with the model by Iain Couzin et al.",
      url='https://www.github.com/benmaier/couzinswarm',
      author='Benjamin F. Maier',
      author_email='bfmaier@physik.hu-berlin.de',
      license='MIT',
      packages=['couzinswarm'],
      install_requires=[
          'numpy>=1.14',
      ],
      zip_safe=False)
