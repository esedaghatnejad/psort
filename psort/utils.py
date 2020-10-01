from pathlib import Path
import yaml
import numpy as np

PROJECT_FOLDER = Path(__file__).parent
CONFIG_FOLDER = PROJECT_FOLDER / 'config'

def read_config(path):
    with open(path) as file:
        config = yaml.full_load(file)

    return config

def get_signal_vars():
    data = read_config(CONFIG_FOLDER / 'gui_config.yml')
    db_vars = {}
    for key, val in data['database_vars'].items():
        if val[0] == 'zeros':
            arrayfun = np.zeros
        elif val[0] == 'full':
            arrayfun = np.full
        else:
            arrayfun = np.array

        db_vars[key] = arrayfun(*val[1:-1], dtype=np.dtype(val[-1]))

    return db_vars

def get_icons():
    data = read_config(CONFIG_FOLDER / 'gui_config.yml')
    return data['icons']
