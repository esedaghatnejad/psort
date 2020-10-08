# psort
purkinjeSort

## Packaging branch
This branch was created by Kyle Poe to begin the process of turning this project into a Python package.

## How to Install
This package is available either through Pypi or the Anaconda ecosystem.

### Pypi (pip) install
`pip install psort`

### Anaconda install
If you have `conda_forge` added as a default channel on your `.condarc`, then

`conda install -c kyle_poe psort`

If you do not, then just do

`conda install -c kyle_poe psort -c conda-forge --strict-channel-priority`

which ensures that only the necessary packages from `conda-forge` are installed through that channel.
