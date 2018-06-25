import pytest

from domain.dao import *

@pytest.fixture
def text_input(request, nlp_ctx):
    t = request.config.getoption('text')
    f = request.config.getoption('file')
    
    ctx = nlp_ctx
    if len(t) > 0:
        ctx.text.import_text(t)
    elif len(f) > 0:
        ctx.text.import_file(f)
    else:
        print('Please specify --file or --text option')

@pytest.fixture
def text_list(request, nlp_ctx):
    ctx = nlp_ctx
    print("")
    print("ID\t\t\t\tContent")
    ctx.text.traverse(
        lambda t: print(t.id+"\t"+t.content)
    )