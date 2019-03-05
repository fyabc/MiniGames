#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Copy data from the given zip file to the project."""

import argparse
import fnmatch
import os
import shutil
import time
import zipfile

__author__ = 'fyabc'

DataDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MyHearthStone')
DataDirName = 'data'
DataFilePattern = '*/resources/*'

_Verbose = False


def _vp(*args, **kwargs):
    if _Verbose:
        print(*args, **kwargs)


def _create_zip(args):
    time_start = time.time()
    basename, ext = os.path.splitext(args.file)
    fmt = ext[1:]
    zip_filename = shutil.make_archive(basename, fmt, root_dir=DataDir, base_dir=DataDirName)
    print(f'Archive data files into {zip_filename!r} in {time.time() - time_start:.6f}s.')


def _load_zip(args):
    time_start = time.time()
    n_files, n_overwrite, n_create = 0, 0, 0

    with zipfile.ZipFile(args.file) as zip_file:
        rc_names = fnmatch.filter((name for name in zip_file.namelist() if not name.endswith('/')), DataFilePattern)
        for name in rc_names:
            _dest_path = os.path.join(DataDir, name)
            _vp('Copying file {} to {} ... '.format(name, _dest_path), end='')

            if os.path.exists(_dest_path):
                n_overwrite += 1
            else:
                n_create += 1

            zip_file.extract(name, path=DataDir)
            n_files += 1
            _vp('done')

    print(f'Copy {n_files} files in {time.time() - time_start:.6f}s '
          f'({n_create} created, {n_overwrite} overwritten).')


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Copy data from data zip file into this project, or create the data zip file from this project.')
    parser.add_argument('file', help='path to data zip file')
    parser.add_argument('-z', '--zip', action='store_true', default=False,
                        help='Create the data zip file instead of copy from it')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Explain what is being done')
    args = parser.parse_args(args)

    global _Verbose
    _Verbose = args.verbose

    if args.zip:
        _create_zip(args)
    else:
        _load_zip(args)


if __name__ == '__main__':
    main()
