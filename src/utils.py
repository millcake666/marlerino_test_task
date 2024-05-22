import os
import sys
import logging
from config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def load_module(module):
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=['object'])


def include_routers(app, app_path, **kwargs):
    path = os.path.join(os.path.dirname(os.path.abspath(app_path)), 'routers')
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.endswith('.py') and not file.startswith('__'):
            module = load_module('routers.{}'.format(file[:-3]))
            try:
                router = getattr(module, 'router')
                app.include_router(router, **kwargs)
                logger.info(f'add router {module}')
                print(f'add router {module}')
            except AttributeError:
                continue
