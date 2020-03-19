#! /usr/bin/env python
# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name
# import argparse
import os
import sys
import shutil
import tempfile
import mmap
import timeit
import secrets


def start():
    chunksize = 1024 * 4096
    total, used, free = shutil.disk_usage(".")
    print("{:,} bytes free space.".format(free))
    try:
        iters = int(free / chunksize)
        #        iters = 10
        leftover = free % chunksize
        #        leftover = 0
        print(
            "Planning for {:,} blocks of {:,} bytes each + {:,} final bytes.".format(
                iters, chunksize, leftover
            )
        )
        tmpdir = tempfile.mkdtemp(dir=".")
        begin = timeit.default_timer()
        for i in range(iters):
            starttime = timeit.default_timer()
            outfile, filename = tempfile.mkstemp(dir=tmpdir)
            print(filename)
            #            time1 = timeit.default_timer()
            mm = mmap.mmap(outfile, chunksize, access=mmap.ACCESS_WRITE)
            #            time2 = timeit.default_timer()
            for j in range(chunksize):
                mm[j] = 0
            mm.flush
            #            time3 = timeit.default_timer()
            for j in range(chunksize):
                mm[j] = 255
            mm.flush
            #            time4 = timeit.default_timer()
            randoms = secrets.token_bytes(chunksize)
            for j in range(chunksize):
                mm[j] = randoms[j]
            mm.flush
            #            time5 = timeit.default_timer()
            mm.close
            os.close(outfile)
            time6 = timeit.default_timer()
            print(
                "{}/{} wrote {} bytes in {:.2f} seconds ({:,} per second)".format(
                    i,
                    iters,
                    chunksize,
                    time6 - starttime,
                    int(chunksize / (time6 - starttime)),
                )
            )
        if leftover > 0:
            outfile, filename = tempfile.mkstemp(dir=tmpdir)
            print(filename)
            mm = mmap.mmap(outfile, leftover)
            randoms = secrets.token_bytes(leftover)
            for j in range(leftover):
                mm[j] = randoms[j]
            print("wrote {:,} bytes".format(leftover))
    except KeyboardInterrupt:
        print("Interrupted")
        mm.flush
        mm.close
        os.close(outfile)
        sys.exit(1)
    except OSError as e:
        print("Got an OSError: {}", format(e))

    end = timeit.default_timer()
    elapsed = end - begin
    rate = int((iters * chunksize) / elapsed)
    total, used, free = shutil.disk_usage(".")
    print("{:,} bytes free space.".format(free))
    print("{:.3f} elapsed, {:,} per second".format(elapsed, rate))


if __name__ == "__main__":
    start()
