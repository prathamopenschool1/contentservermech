"""
#Django logger settings for pos project.
"""

import os
from pathlib import Path


tmp_path = os.path.join(str(Path.home()), 'tmp')


# In RPI case
# tmp_path = '/home/pi'
tmp_path = os.path.join(tmp_path, 'tmp')
print("tmp_path ", tmp_path)

if not os.path.exists(tmp_path):
	os.mkdir(tmp_path)

LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'formatters':{
		'large':{
			'format':'%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
		},
		'tiny':{
			'format':'%(asctime)s  %(message)s  '
		}
	},
	'handlers':{
		'errors_file':{
			'level':'ERROR',
		       'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			# 'filename':'/home/pi/tmp/errordebug.log',
			'filename': os.path.join(tmp_path, 'errordebug.log'),
			'formatter':'large',
		},
		'info_file':{
			'level':'INFO',
		       'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			# 'filename':'/home/pi/tmp/infoLogger.log',
			'filename':os.path.join(tmp_path, 'infoLogger.log'),
			'formatter':'large',
		},
	},
	'loggers':{
		'error_logger':{
			'handlers':['errors_file'],
			'level':'WARNING',
			'propagate':False,
		},
		'info_logger':{
			'handlers':['info_file'],
			'level':'INFO',
			'propagate':False,
		},
	},
}
