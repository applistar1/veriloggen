from __future__ import absolute_import
from __future__ import print_function

import os
import sys


import veriloggen

import thread_stream_verify

size = 32


def test(request):
    veriloggen.reset()

    simtype = request.config.getoption('--sim')

    rslt = thread_stream_verify.run(size,
                                    filename=None, simtype=simtype)

    verify_rslt = rslt.splitlines()[-1]
    assert(verify_rslt == '# verify: PASSED')


if __name__ == '__main__':
    rslt = thread_stream_verify.run(size,
                                    filename='tmp.v')
    print(rslt)