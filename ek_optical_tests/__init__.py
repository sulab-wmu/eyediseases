#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os


def data_path(test_file=None):
    test_data_path = os.path.dirname(os.path.realpath(__file__))
    if test_data_path:
        return os.path.join(test_data_path, test_file)
    else:
        return test_data_path
