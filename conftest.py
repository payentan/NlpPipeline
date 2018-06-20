import pytest
from domain.dao import NlpContext

def pytest_addoption(parser):
    parser.addoption('--tid', action='store', default='abc', help='Text id to process')

    parser.addoption('--text', action='store', default='', help='text content')

    parser.addoption('--file', action='store', default='', help='text file')


_nlp_ctx = NlpContext()

@pytest.fixture(scope="session")
def nlp_ctx():
    return _nlp_ctx