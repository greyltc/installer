import os

from installer.__main__ import _get_scheme_dict as get_scheme_dict
from installer.__main__ import _main as main


def test_get_scheme_dict():
    d = get_scheme_dict(distribution_name="foo")
    assert set(d.keys()) >= {"purelib", "platlib", "headers", "scripts", "data"}


def test_get_scheme_dict_prefix():
    d = get_scheme_dict(distribution_name="foo", prefix="/foo")
    for key in ("purelib", "platlib", "headers", "scripts", "data"):
        assert d[key].startswith(
            f"{os.sep}foo"
        ), f"{key} does not start with /foo: {d[key]}"


def test_get_scheme_dict_prefix_scheme():
    d = get_scheme_dict(distribution_name="foo", prefix="/foo", scheme="posix_prefix")
    for key in ("purelib", "platlib", "headers", "scripts", "data"):
        assert d[key].startswith(
            f"{os.sep}foo"
        ), f"{key} does not start with /foo: {d[key]}"


def test_get_scheme_dict_scheme():
    d = get_scheme_dict(distribution_name="foo", scheme="posix_prefix")
    assert set(d.keys()) >= {"purelib", "platlib", "headers", "scripts", "data"}


def test_main(fancy_wheel, tmp_path):
    destdir = tmp_path / "dest"

    main([str(fancy_wheel), "-d", str(destdir)], "python -m installer")

    installed_py_files = destdir.rglob("*.py")

    assert {f.stem for f in installed_py_files} == {"__init__", "__main__", "data"}

    installed_pyc_files = destdir.rglob("*.pyc")
    assert {f.name.split(".")[0] for f in installed_pyc_files} == {
        "__init__",
        "__main__",
    }


def test_main_prefix(fancy_wheel, tmp_path):
    destdir = tmp_path / "dest"

    main([str(fancy_wheel), "-d", str(destdir), "-p", "/foo"], "python -m installer")

    installed_py_files = list(destdir.rglob("*.py"))

    for f in installed_py_files:
        assert str(f.parent).startswith(
            str(destdir / "foo")
        ), f"path does not respect destdir+prefix: {f}"
    assert {f.stem for f in installed_py_files} == {"__init__", "__main__", "data"}

    installed_pyc_files = destdir.rglob("*.pyc")
    assert {f.name.split(".")[0] for f in installed_pyc_files} == {
        "__init__",
        "__main__",
    }


def test_main_no_pyc(fancy_wheel, tmp_path):
    destdir = tmp_path / "dest"

    main(
        [str(fancy_wheel), "-d", str(destdir), "--no-compile-bytecode"],
        "python -m installer",
    )

    installed_py_files = destdir.rglob("*.py")

    assert {f.stem for f in installed_py_files} == {"__init__", "__main__", "data"}

    installed_pyc_files = destdir.rglob("*.pyc")
    assert set(installed_pyc_files) == set()
