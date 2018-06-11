from __future__ import absolute_import
from __future__ import print_function

import veriloggen
import thread_axi_dma_long_narrow


def test(request):
    veriloggen.reset()

    simtype = request.config.getoption('--sim')

    rslt = thread_axi_dma_long_narrow.run(filename=None, simtype=simtype)

    verify_rslt = rslt.splitlines()[-1]
    assert(verify_rslt == '# verify: PASSED')
