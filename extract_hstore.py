#! /usr/bin/env python3
print("importing...")
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target")
parser.add_argument("--table")
args = parser.parse_args()
target = args.target
table = args.table

# Per <https://stackoverflow.com/a/56152470>
from sqlalchemy.dialects.postgresql import HSTORE

print("Extracting hstore...")

hstore_to_dict = HSTORE().result_processor(None, None)

create = (
    f"CREATE TABLE {table}_fid_to_tag("
    "ogc_fid INTEGER, key VARCHAR, value VARCHAR,"
    f" FOREIGN KEY(ogc_fid) REFERENCES {table}(ogc_fid));"
)
select = f"SELECT ogc_fid, other_tags FROM {table} WHERE other_tags IS NOT NULL;"
insert = f"INSERT INTO {table}_fid_to_tag VALUES(?, ?, ?);"

import sqlite3

conn = sqlite3.connect(target)

conn.execute(create)
for fid, tags in conn.execute(select).fetchall():
    for key, value in hstore_to_dict(tags).items():
        conn.execute(insert, (fid, key, value)) and None

conn.commit()  # required by close()
conn.close()
