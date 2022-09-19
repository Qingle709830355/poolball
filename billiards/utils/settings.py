from pathlib import Path


import billiards as bl


BASEDIR = Path(bl.__file__).parent
ASSET_PATH = BASEDIR / "asset"
CONFIG_PATH = BASEDIR / "config"

