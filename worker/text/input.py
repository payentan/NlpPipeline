import pytest

from domain.dao import *

@pytest.fixture
def text_input(request):
    t = request.config.getoption('text')
    f = request.config.getoption('file')
    
    node = NodeText()
    if len(t) > 0:
        node.import_text(t)
    elif len(f) > 0:
        node.import_file(f)