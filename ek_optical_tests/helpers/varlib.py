#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import ctypes
import inspect
import os


class dicttemp:
    def __init__(self, obj, changes):
        self.obj = obj
        self.save = {}
        for var, val in changes.items():
            if var in obj:
                self.save[var] = obj[var]
            else:
                self.save[var] = None
            self.obj[var] = val

    def __enter__(self):
        pass

    def __exit__(self, type, val, trace):
        for var, val in self.save.items():
            if val is not None:
                self.obj[var] = val
            else:
                del self.obj[var]


class envtemp(dicttemp):
    def __init__(self, changes):
        super().__init__(os.environ, changes)


class vartemp:
    def __init__(self, changes):
        self.frame = inspect.stack()[1][0]
        self.f_locals = {}
        self.f_globals = {}
        for var, val in changes.items():
            if var in self.frame.f_locals:
                self.f_locals[var] = self.frame.f_locals[var]
                self.frame.f_locals[var] = val
            elif var in self.frame.f_globals:
                self.f_globals[var] = self.frame.f_globals[var]
                self.frame.f_globals[var] = val
            ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(self.frame), ctypes.c_int(0))

    def __enter__(self):
        pass

    def __exit__(self, type, val, trace):
        for var, val in self.f_locals.items():
            self.frame.f_locals[var] = val
        for var, val in self.f_globals.items():
            self.frame.f_globals[var] = val
        ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(self.frame), ctypes.c_int(0))


import unittest

_test_y = 4


class TestVarLib(unittest.TestCase):
    def test_local(self):
        x = 4
        with vartemp({'x': 5}):
            self.assertEqual(x, 5)
        self.assertEqual(x, 4)

    def test_mixed(self):
        global _test_y
        x = 4
        _test_y = 4
        with vartemp({'x': 5, '_test_y': 5}):
            self.assertEqual(x, 5)
            self.assertEqual(_test_y, 5)
        self.assertEqual(x, 4)
        self.assertEqual(_test_y, 4)

    def test_env(self):
        os.environ['FOO'] = '4'
        with envtemp({'FOO': '5', 'BAR': '5'}):
            self.assertEqual(os.environ['FOO'], '5')
            self.assertEqual(os.environ['BAR'], '5')
        self.assertEqual(os.environ['FOO'], '4')
        self.assertTrue('BAR' not in os.environ)
