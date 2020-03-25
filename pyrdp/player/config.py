#
# This file is part of the PyRDP project.
# Copyright (C) 2020 GoSecure Inc.
# Licensed under the GPLv3 or later.
#

DEFAULTS = """
[vars]
output_dir = pyrdp_output
log_dir = logs
level      = INFO

[logs]
version = 1
filter = pyrdp
notifications = True

[logs:loggers:pyrdp]
handlers = console, player
level = ${vars:level}

[logs:handlers:console]
class     = logging.StreamHandler
formatter = default
stream    = ext://sys.stderr

[logs:handlers:player]
class     = logging.handlers.RotatingFileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/player.log
formatter = default

[logs:formatters:default]
class: logging.Formatter
format = [{asctime}] - {levelname} - {name} - {message}
style = {
"""
