#
# This file is part of the PyRDP project.
# Copyright (C) 2020 GoSecure Inc.
# Licensed under the GPLv3 or later.
#
from configparser import ConfigParser, ExtendedInterpolation

import appdirs
CONFIG_DIR = appdirs.user_config_dir("pyrdp", "pyrdp")


def load(path: str, fallback: str) -> ConfigParser:
    """
    Retrieve the PyRDP settings from a file

    :param path: The path of the file to load.
    :param fallback: The fallback configuration.

    :returns: A dict of the settings or None if the file was not present.

    """
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.optionxform = str
    try:
        if len(config.read(path)) > 0:
            return config
    except Exception:
        # Fallback to default settings..
        pass

    config.read_string(fallback)
    return config
