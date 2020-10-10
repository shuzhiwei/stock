#!/usr/bin/env python
# coding=utf-8

import logging
from logging import handlers
import platform

LOGGER_NAME = 'stock'

if platform.system()=='Windows':
    LOGGER_FILE = './stock.log'
else:
    LOGGER_FILE = '/tmp/stock.log'
    
logging.basicConfig(filemode='a')
logger = logging.getLogger(LOGGER_NAME)
#th = handlers.TimedRotatingFileHandler(filename=LOGGER_FILE, when='D', backupCount=10, encoding='utf-8')
th = handlers.RotatingFileHandler(filename=LOGGER_FILE, mode='a', maxBytes=50*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
th.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(th)
