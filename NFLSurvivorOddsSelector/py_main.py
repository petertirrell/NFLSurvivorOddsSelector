# -*- coding: utf-8 -*-
"""Application or script description"""
import logging
import logging.config
import sys
from config import *

# logging setup
logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('root')
# end logging setup

def main(argv):
    """Main entry point for the script."""
    logger.debug('Enter application')
    logger.debug('Secret config 1: {0}'.format(SECRET1))
    logger.debug('Secret config 2: {0}'.format(SECRET2))
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
