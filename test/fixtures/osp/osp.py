from pathlib           import Path
from rohdeschwarz.yaml import load_yaml


# paths
root_path   = Path(__file__).parent.resolve()
driver_file = root_path / 'driver.yaml'
path_file   = root_path / 'path.yaml'


# read fixtures

driver = load_yaml(driver_file)
path   = load_yaml(path_file)
