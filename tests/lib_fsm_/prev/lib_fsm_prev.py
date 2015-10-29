import sys
import os

from veriloggen import *

def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')
    valid = m.OutputReg('valid', initval=0)

    fsm = lib.FSM(m, 'fsm')
    
    for i in range(2):
        fsm.goto_next()

    # assert valid, then de-assert at the next cycle
    fsm.add( valid(1), cond=fsm.prev(valid, 1)==0 )
    fsm.add( valid(0), delay=1 )
    fsm.goto_next( cond=fsm.prev(valid, 1)==1 )
    
    for i in range(4):
        fsm.goto_next()

    # assert valid, then de-assert at the next cycle if not asserted again
    for i in range(4):
        fsm.add( valid(1) )
        fsm.add( valid(0), delay=1 )
        fsm.goto_next()
    
    fsm.make_always(clk, rst)

    return m

def mkTest():
    m = Module('test')
    clk = m.Reg('CLK')
    rst = m.Reg('RST')
    valid = m.Wire('valid')

    uut = m.Instance(mkLed(), 'uut',
                     ports=(('CLK', clk), ('RST', rst), ('valid', valid)))

    lib.simulation.setup_waveform(m, uut)
    lib.simulation.setup_clock(m, clk, hperiod=5)
    init = lib.simulation.setup_reset(m, rst, period=100)

    init.add(
        Delay(1000),
        Systask('finish'),
    )

    return m
    
if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)