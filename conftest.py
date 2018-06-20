import pytest
from domain.dao import NlpContext

connect('nlppipeline')

def pytest_addoption(parser):
    parser.addoption('--tid', action='store', default='abc', help='Text id to process')

    parser.addoption('--text', action='store', default='', help='text content')

    parser.addoption('--file', action='store', default='', help='text file')

@pytest.fixture(scope="session")
def nlp_ctx():
    return NlpContext()