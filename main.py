import asyncio
import logging
from functools import wraps

from wb_parser_bot import load

def run_decorator(setup_function):
    @wraps(setup_function)
    def wrapper(*args, **kwargs):
        setup_function(*args, **kwargs)
        asyncio.run(load())
    
    return wrapper

@run_decorator
def run_dev():
    logging.basicConfig(level=logging.DEBUG)

@run_decorator
def run_prod():
    logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    run_dev()