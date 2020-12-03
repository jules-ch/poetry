import shutil
import pytest


@pytest.fixture
def tester(command_tester_factory):
    return command_tester_factory("build")


def test_build(tester, fixture_dir):
    demo = fixture_dir("git") / "github.com" / "demo" / "demo"
    tester.execute()
    expected = """\
Building simple-project (1.2.3)
  - Building sdist
  - Built simple-project-1.2.3.tar.gz
  - Building wheel
  - Built simple_project-1.2.3-py2.py3-none-any.whl
"""

    assert expected == tester.io.fetch_output()


def test_build_sdist(app, tester):
    tester.execute("-f sdist")
    expected = """\
Building simple-project (1.2.3)
  - Building sdist
  - Built simple-project-1.2.3.tar.gz
"""

    assert expected == tester.io.fetch_output()


def test_build_wheel(tester):
    tester.execute("-f wheel")
    expected = """\
Building simple-project (1.2.3)
  - Building wheel
  - Built simple_project-1.2.3-py2.py3-none-any.whl
"""

    assert expected == tester.io.fetch_output()