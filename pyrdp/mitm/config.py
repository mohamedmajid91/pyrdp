#
# This file is part of the PyRDP project.
# Copyright (C) 2019 GoSecure Inc.
# Licensed under the GPLv3 or later.
#

from pathlib import Path
from typing import Optional


class MITMConfig:
    """
    Configuration options for the RDP MITM.
    """

    def __init__(self):
        self.targetHost: str = None
        """The RDP server"""

        self.targetPort: int = None
        """The RDP server's port"""

        self.certificateFileName: str = None
        """Path to the TLS certificate"""

        self.privateKeyFileName: str = None
        """Path to the TLS private key"""

        self.attackerHost: Optional[str] = None
        """The attacker host"""

        self.attackerPort: Optional[int] = None
        """The attacker port"""

        self.replacementUsername: str = None
        """The replacement username for login attempts"""

        self.replacementPassword: str = None
        """The replacement password for login attempts"""

        self.outDir: Path = None
        """The output directory"""

        self.recordReplays: bool = True
        """Whether replays should be recorded or not"""

        self.downgrade: bool = True
        """Whether to actively downgrade unsupported extensions."""

        self.payload: str = ""
        """Payload to send automatically upon connection"""

        self.payloadDelay: int = None
        """Delay before sending payload automatically, in milliseconds"""

        self.payloadDuration: int = None
        """Amount of time the payload should take to complete, in milliseconds"""

        self.enableCrawler: bool = False
        """Whether the crawler should be enabled or not"""

        self.crawlerMatchFileName: str = None
        """Path to the crawler match configuration file"""

        self.crawlerIgnoreFileName: str = None
        """Path to the crawler ignore configuration file"""

        self.disableActiveClipboardStealing: bool = False
        """ If set to False, use PassiveClipboardStealer instead of ActiveClipboardStealer."""

    @property
    def replayDir(self) -> Path:
        """
        Get the directory for replay files.
        """
        return self.outDir / "replays"

    @property
    def fileDir(self) -> Path:
        """
        Get the directory for intercepted files.
        """
        return self.outDir / "files"

"""
The default MITM configuration settings.
"""
DEFAULTS = """
[vars]
sensor_id = PyRDP
log_dir = logs
output_dir = pyrdp_output
level      = INFO

[logs]
version = 1
filter = pyrdp

[logs:loggers:pyrdp]
handlers = console, mitm
level = ${vars:level}

[logs:loggers:pyrdp.mitm.connections]
handlers = connections
level    = ${vars:level}

[logs:loggers:crawler]
handlers = crawl_json, crawl_txt
level    = ${vars:level}

[logs:loggers:ssl]
handlers = ssl, ssl_console
level    = DEBUG

[logs:handlers:console]
class     = logging.StreamHandler
formatter = default
stream    = ext://sys.stderr

[logs:handlers:mitm]
class     = logging.handlers.TimedRotatingFileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/mitm.log
when      = D
formatter = default

[logs:handlers:connections]
class     = logging.FileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/mitm.json
formatter = json

[logs:handlers:crawl_txt]
class     = logging.FileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/crawl.log
formatter = compact

[logs:handlers:crawl_json]
class     = logging.FileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/crawl.json
formatter = json

[logs:handlers:ssl]
class     = logging.FileHandler
filename  = ${vars:output_dir}/${vars:log_dir}/ssl.log
formatter = ssl

[logs:handlers:ssl_console]
class     = logging.StreamHandler
stream    = ext://sys.stderr
formatter = ssl

[logs:formatters:default]
() = pyrdp.logging.formatters.VariableFormatter
fmt = [{asctime}] - {levelname} - {sessionID} - {name} - {message}
style = {

[logs:formatters:default:defaultVariables]
sessionID = GLOBAL

[logs:formatters:json]
() = pyrdp.logging.formatters.JSONFormatter

[logs:formatters:json:baseDict]
sensor = ${vars:sensor_id}

[logs:formatters:compact]
() = pyrdp.logging.formatters.VariableFormatter
fmt = [{asctime}] - {sessionID} - {message}
style = {

[logs:formatters:compact:defaultVariables]
sessionID = GLOBAL

[logs:formatters:ssl]
() = pyrdp.logging.formatters.SSLSecretFormatter
"""
