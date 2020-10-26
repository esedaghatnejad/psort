from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='psort',
      version='0.4.32',
      description='PurkinjeSort',
      long_description=long_description,
      url='https://github.com/esedaghatnejad/psort',
      author='Ehsan Sedaghat-Nejad',
      author_email='esedaghatnejad@gmail.com',
      license='GPL',
      packages=find_packages(),
      package_data={
            'psort': ['icons/*.png', 'LICENSE'],
      },
      entry_points={
            'console_scripts': [
                'psort = psort.__main__:run_from_cmdline',
            ],
      },
      install_requires=[
            'pyqt5>=5.11.2',
            'numpy>=1.19.1',
            'matplotlib>=3.3.1',
            'numba>=0.50.1',
            'scipy>=1.5.2',
            'h5py>=2.10.0',
            'pyqtgraph>=0.11.0',
            'scikit-learn>=0.23.2',
      ],
      scripts=['bin/psort'],
      zip_safe=False,
      python_requires='>=3.7',
)
