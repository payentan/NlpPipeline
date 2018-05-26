import pytest
from domain.persist import *

connect('nlppipeline')

def pytest_addoption(parser):
    parser.addoption('--tid', action='store', default='abc', help='Text id to process')