import base64
import contextlib
import json
import os
import shutil
import tempfile
import unittest

from path2json.main import main

@contextlib.contextmanager
def make_case(d):
    path = tempfile.mkdtemp()
    output = tempfile.mktemp()
    writecase(path, d)
    yield path, output
    shutil.rmtree(path, ignore_errors=True)
    os.remove(output)


def writecase(path, d):
    for k in d:
        kpath = os.path.join(path, k)
        if isinstance(d[k], dict):
            os.mkdir(kpath)
            writecase(kpath, d[k])
            continue
        with open(kpath, "wb") as fd:
            if isinstance(d[k], int):
                fd.write(b"%d" % d[k])
            else:
                fd.write(d[k])


class TestMain(unittest.TestCase):

    def test_00_00_nothing(self):
        with make_case({}) as (path, output):
            main([path, output])
            with open(output) as fd:
                result = json.load(fd)
            self.assertDictEqual(result, {})

    def test_01_01_int(self):
        case = dict(foo=1)
        with make_case(case) as (path, output):
            main([path, output])
            with open(output) as fd:
                result = json.load(fd)
            self.assertDictEqual(result, case)

    def test_01_02_blob(self):
        case = dict(foo=b"hello")
        with make_case(case) as (path, output):
            main([path, output])
            with open(output) as fd:
                result = json.load(fd)
            self.assertEqual(len(result), 1)
            self.assertEqual(result["foo"].encode(),
                             case["foo"])

    def test_02_00_no_recursive(self):
        case = dict(foo=dict(f1=1), bar=dict(f2=b"hello"))
        with make_case(case) as (path, output):
            main([path, output])
            with open(output) as fd:
                result = json.load(fd)
            self.assertDictEqual(result, {})

    def test_02_01_recursive(self):
        case = dict(foo=dict(f1=1), bar=dict(f2=b"hello"))
        for switch in ("-r", "--recursive"):
            with make_case(case) as (path, output):
                main([switch, path, output])
                with open(output) as fd:
                    result = json.load(fd)
                self.assertDictEqual(result["foo"], case["foo"])
                self.assertEqual(
                    result["bar"]["f2"].encode("ascii"),
                    case["bar"]["f2"])

    def test_03_00_no_link(self):
        case = dict(foo=1)
        with make_case(case) as (path, output):
            os.symlink(os.path.join(path, "foo"), os.path.join(path, "bar"))
            main([path, output])
            with open(output) as fd:
                result = json.load(fd)
            self.assertDictEqual(result, case)

    def test_03_01_link(self):
        case = dict(foo=1)
        with make_case(case) as (path, output):
            os.symlink(os.path.join(path, "foo"), os.path.join(path, "bar"))
            for switch in ("-l", "--follow-link"):
                main([switch, path, output])
                with open(output) as fd:
                    result = json.load(fd)
                self.assertDictEqual(result, dict(foo=1, bar=1))
