# the scope of this file
# python bulk_insert.py table_name csv_file.csv

import threading
import sys

def runner(fname, iteration):
    global lck
    lck.acquire()
    with open(fname, 'a') as f:
        f.write("TEST " + str(iteration) + '\n')
    lck.release()

lck = threading.Lock()

# filename to use
fname = sys.argv[1] if len(sys.argv) > 1 else 'counter.txt'

with open(fname, 'w') as f:
    f.write('0\n')

threads = []
for i in xrange(0, 20):
    t = threading.Thread(target = runner, args = (fname, i))
    t.start()

for t in threads:
    t.join()