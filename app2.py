import sys
import PySimpleGUI as gui
from scripts.py.application import logger

name = str(__name__)

name = name[2:-2]

log = logger.setup_logger(name)
log.info('Done!')

print(sys.path)