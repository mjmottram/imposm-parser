# Copyright 2011 Omniscale GmbH & Co. KG
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import multiprocessing
import sys
import bz2

try:
    from setproctitle import setproctitle
    setproctitle
except ImportError:
    setproctitle = lambda x: None


PY3 = sys.version_info[0] == 3


def default_concurrency():
    return multiprocessing.cpu_count()

@contextlib.contextmanager
def fileinput(filename):
    if filename.endswith('bz2'):
        if PY3:
            fh = bz2.open(filename, 'rt')
        else:
            fh = bz2.BZ2File(filename, 'r')
        yield fh
        fh.close()
    else:
        fh = open(filename, 'r')
        yield fh
        fh.close()

def estimate_records(files):
    records = 0
    for f in files:
        fsize = os.path.getsize(f)
        if f.endswith('.bz2'):
            fsize *= 11 # observed bzip2 compression factor on osm data
        if f.endswith('.pbf'):
            fsize *= 15 # observed pbf compression factor on osm data
        records += fsize/200
    
    return int(records)