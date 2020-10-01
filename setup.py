from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='psort',
      version='0.4.26.a',
      description='Graphical application for identifying simple and complex purkinje spikes',
      long_description=readme(),
      url='https://github.com/esedaghatnejad/psort',
      author='Ehsan Sedaghat-Nejad',
      author_email='esedagh1@jhu.edu',
      license='GPL',
      packages=find_packages(),
      entry_points={
            'console_scripts': [
                'psort = psort.main:run_from_cmdline',
            ],
      },
      package_data={
            'psort': ['icons/*.png'],
      },
      install_requires=[            # NOTE: This is EXTREMELY strict, and we should
            'deepdish==0.3.5',      # allow more versions for future robustness.
            'neo==0.8.0',
            'pymatreader==0.0.23',
            'umap-learn==0.4.6',
            'pyqt5~=5.11.2',
            'numpy==1.19.1',
            'matplotlib==3.3.1',
            'numba~=0.50.1',
            'scipy==1.5.2',
            'h5py==2.10.0',
            'pyqtgraph==0.11.0',
            'scikit-learn==0.23.2',
            'umap-learn==0.4.6',
      ],
      scripts=['bin/psort'],
      # include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7',
)