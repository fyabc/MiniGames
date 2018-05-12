#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Copy data from the given zip file to the project."""

import argparse
import fnmatch
import os
import time
import zipfile

__author__ = 'fyabc'

DataDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MyHearthStone')
DataFilePattern = '*/resources/*'


def main(args=None):
    parser = argparse.ArgumentParser(description='Copy data from data zip file into this project.')
    parser.add_argument('file', help='path to data zip file')
    args = parser.parse_args(args)

    time_start = time.time()
    n_files = 0

    with zipfile.ZipFile(args.file) as zip_file:
        rc_names = fnmatch.filter((name for name in zip_file.namelist() if not name.endswith('/')), DataFilePattern)
        for name in rc_names:
            print('Copying file {} to {} ... '.format(name, os.path.join(DataDir, name)), end='')
            zip_file.extract(name, path=DataDir)
            n_files += 1
            print('done')

    print('Copy {} files in {:.6f}s.'.format(n_files, time.time() - time_start))


if __name__ == '__main__':
    main()
