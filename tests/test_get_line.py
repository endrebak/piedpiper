
import pytest

from piedpiper.main import _get_statement

@pytest.fixture
def f(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"

    content = """hi.im().a[["method"]].chain()"""

    p.write_text(content)

    return str(p)



@pytest.fixture
def f(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"

    content = """(hi
                 .im()
                 .a[["method"]]
                 .chain())"""

    p.write_text(content)

    return str(p)


def test_get_line(f):

    line_no = 0

    result = _get_statement(f, line_no)

    print(result)

    assert result == '''hi.im().a[["method"]].chain()'''
