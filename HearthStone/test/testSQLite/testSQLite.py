#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sqlite3

__author__ = 'fyabc'


def _test():
    conn = sqlite3.connect(':memory:')

    cur = conn.cursor()

    cur.execute('''\
CREATE TABLE Test (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(255)
);
''')

    cur.executemany('''\
INSERT INTO Test VALUES (?, ?);
''', [
        (0, 'James'),
        (1, 'David'),
        (2, 'Allen'),
        (3, 'Teddy'),
    ])

    cur.execute('''\
SELECT * FROM Test;
''')

    for row in cur.fetchall():
        print(row)


if __name__ == '__main__':
    _test()
