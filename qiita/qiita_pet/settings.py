#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, The QiiTa-pet Project"
__credits__ = ["Joshua Shorenstein", "Antonio Gonzalez",
               "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "Joshua.Shorenstein@colorado.edu"
__status__ = "Development"

# import logging
# import sys
# #log linked to the standard error stream
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)-8s - %(message)s',
#                     datefmt='%d/%m/%Y %Hh%Mm%Ss')
# console = logging.StreamHandler(sys.stderr)

#analyses available in QIIME. Don't forget the options template!
SINGLE = [
    # 'TopiaryExplorer_Visualization',
    # 'Heatmap',
    # 'Taxonomy_Summary',
    'Alpha_Diversity',
    'Beta_Diversity',
    ]

COMBINED = [
    'Procrustes',
    # 'Network_Analysis',
    ]

# All push messages are in json format. They must have the following format:
# 'analysis': analysis name
# 'msg': message to print
# 'job': what job this is from in format datatype:job_function
# 'results': list of files created if any
