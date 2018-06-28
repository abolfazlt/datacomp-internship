#!/usr/bin/env python3

import logging.handlers
import os
import sqlite3
import sys
import time

import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler('logs/judge.log', maxBytes=1024 * 1024 * 10, backupCount=10),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

EPS = np.finfo(np.float64).eps
PATH = os.path.dirname(os.path.realpath(__file__))
MEDIA_PATH = os.path.join(PATH, 'media')


def judge(con, row_id, file, is_final):
    try:
        with con:
            con.execute('UPDATE visage_submission SET status = \'P\' WHERE id = ?;', (row_id,))

        ans_file = 'ans_final.csv' if is_final else 'ans.csv'
        ans = np.log10(np.loadtxt(os.path.join(PATH, ans_file), delimiter=',', dtype=np.float64) + EPS)
        res = np.log10(np.loadtxt(os.path.join(MEDIA_PATH, file), delimiter=',', dtype=np.float64) + EPS)
        error = np.sqrt(np.mean(np.power(np.subtract(np.nan_to_num(res), np.nan_to_num(ans)), 2)))
        logger.info('[{id}] Error: {error}'.format(id=row_id, error=error))

        with con:
            con.execute('UPDATE visage_submission SET status = \'J\', error = ? WHERE id = ?;', (error, row_id))
    except (sqlite3.Error, ValueError) as e:
        logger.error(e)
        with con:
            con.execute('UPDATE visage_submission SET status=\'E\' WHERE id = ?;', (row_id,))


def main():
    try:
        con = sqlite3.connect('datacomp.sqlite3')
    except sqlite3.Error as e:
        logger.error(e)
        exit(1)

    while True:
        r = con.execute('SELECT id, file, is_final FROM visage_submission WHERE status = \'S\' ORDER BY timestamp ASC;')
        for row in r:
            judge(con, row[0], row[1], row[2])
        time.sleep(10)


if __name__ == '__main__':
    main()
