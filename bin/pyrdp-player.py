#!/usr/bin/env python3

#
# This file is part of the PyRDP project.
# Copyright (C) 2018-2020 GoSecure Inc.
# Licensed under the GPLv3 or later.
#

# asyncio needs to be imported first to ensure that the reactor is
# installed properly. Do not re-order.
import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install(asyncio.get_event_loop())

from pyrdp.player import HAS_GUI

import argparse
import logging
import logging.handlers
import sys
import os

if HAS_GUI:
    from pyrdp.player import MainWindow
    from PySide2.QtWidgets import QApplication

from pyrdp.logging import LOGGER_NAMES, NotifyHandler, configure as configureLoggers
from pyrdp.player.config import DEFAULTS
from pyrdp.core import settings

LOG = logging.getLogger(LOGGER_NAMES.PYRDP)



def enableNotifications():
    """Enable notifications if supported."""
    if not headless and HAS_GUI:
        # https://docs.python.org/3/library/os.html
        if os.name != "nt":
            try:
                notifyHandler = NotifyHandler()
		notifyHandler.setFormatter(logging.Formatter("[{asctime}] - {message}", style = "{"))


                uiLogger = logging.getLogger(LOGGER_NAMES.PLAYER_UI)
                uiLogger.addHandler(notifyHandler)
            except Exception:
                # No notification daemon or DBus, can't use notifications.
                pass
        else:
            LOG.warning("Notifications are not supported for your platform, they will be disabled.")


def main():
    """
    Parse the provided command line arguments and launch the GUI.
    :return: The app exit code (0 for normal exit, non-zero for errors)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("replay", help="Replay files to open on launch (optional)", nargs="*")
    parser.add_argument("-b", "--bind", help="Bind address (default: 127.0.0.1)", default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Bind port (default: 3000)", default=3000)
    parser.add_argument("--headless", help="Parse a replay without rendering the user interface.", action="store_true")
    parser.add_argument("-o", "--output", help="Output folder", default=None)
    parser.add_argument("-L", "--log-level", help="Log level", default=None, choices=["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"], nargs="?")
    parser.add_argument("-F", "--log-filter", help="Only show logs from this logger name (accepts '*' wildcards)", default=None)
    args = parser.parse_args()

    cfg = settings.load(f'{settings.CONFIG_DIR}/player.ini', DEFAULTS)

    # Modify configuration with switches.
    if args.log_level:
        cfg.set('vars', 'level', args.log_level)
    if args.log_filter:
        cfg.set('logs', 'filter', args.log_filter)
    if args.output:
        cfg.set('vars', 'output_dir', args.output)

    configureLoggers(cfg)
    if cfg.getboolean('logs', 'notifications', fallback=False):
        enableNotifications()

    if not HAS_GUI and not args.headless:
        LOG.error('Headless mode is not specified and PySide2 is not installed. Install PySide2 to use the graphical user interface.')
        sys.exit(127)

    if not args.headless:
        app = QApplication(sys.argv)
        mainWindow = MainWindow(args.bind, int(args.port), args.replay)
        mainWindow.show()

        return app.exec_()
    else:
        LOG.info('Starting PyRDP Player in headless mode.')
        from pyrdp.player import HeadlessEventHandler
        from pyrdp.player.Replay import Replay
        processEvents = HeadlessEventHandler()
        for replay in args.replay:
            processEvents.output.write(f'== REPLAY FILE: {replay}\n')
            fd = open(replay, "rb")
            replay = Replay(fd, handler=processEvents)
            processEvents.output.write('\n-- END --------------------------------\n')


if __name__ == '__main__':
    sys.exit(main())
