import MyPath

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(lineno)d %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',  # 控制台日志级别
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': MyPath.LOG_FILE,
            'formatter': 'default',
            'level': 'DEBUG',  # 文件日志级别
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        # logic包的日志配置
        'logic': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        # 'another_package': {  # 另一个包名
        #     'level': 'ERROR',
        #     'handlers': ['console', 'file'],
        #     'propagate': False,
        # },
    }
}