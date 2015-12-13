from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import copy

import veriloggen.core.vtypes as vtypes
from veriloggen.core.module import Module
from veriloggen.seq.seq import Seq

from . import visitor
from . import dtypes
from . import scheduler
from . import allocator

class Dataflow(object):
    def __init__(self, *nodes, **opts):
        self.datawidth = opts['datawidth'] if 'datawidth' in opts else 32
        self.nodes = set(nodes)
        
    def add(self, *nodes):
        self.nodes.extend(nodes)
    
    def implement(self, m, clock, reset, name=None, aswire=False):
        """ implemente actual registers and operations in Verilog """
            
    def to_module(self, name, clock='CLK', reset='RST'):
        """ generate a Module definion """
        
        m = Module(name)
        clk = m.Input(clock)
        rst = m.Input(reset)
        seq = Seq(m, 'seq', clk, rst)

        dataflow_nodes = copy.deepcopy(self.nodes)
        
        input_visitor = visitor.InputVisitor()
        input_vars = set()
        for node in dataflow_nodes:
            input_vars.update( input_visitor.visit(node) )

        output_visitor = visitor.OutputVisitor()
        output_vars = set()
        for node in dataflow_nodes:
            output_vars.update( output_visitor.visit(node) )

        # add input ports
        for input_var in sorted(input_vars, key=lambda x:x.input_data):
            input_var._implement_input(m, seq)

        # schedule
        sched = scheduler.ASAPScheduler()
        sched.schedule(output_vars)
        
        # balance output stage depth
        max_stage = None
        for var in output_vars:
            max_stage = dtypes.max(max_stage, var.end_stage)

        output_vars = sched.balance_output(output_vars, max_stage)

        # get all vars
        all_visitor = visitor.AllVisitor()
        all_vars = set()
        for var in output_vars:
            all_vars.update( all_visitor.visit(var) )

        # allocate (implement signals)
        alloc = allocator.Allocator()
        alloc.allocate(m, seq, all_vars)

        # add output ports
        for output_var in sorted(output_vars, key=lambda x:x.output_data):
            output_var._implement_output(m, seq)

        # add always statement
        seq.make_always()

        return m

    #---------------------------------------------------------------------------
    # Add a new variable
    #---------------------------------------------------------------------------
    def Constant(self, value):
        raise NotImplementedError()
    
    def Variable(self, name=None, valid=None, ready=None):
        raise NotImplementedError()
    
    def Iadd(self, data, init=None, reset=None):
        raise NotImplementedError()
    
    def Isub(self, data, init=None, reset=None):
        raise NotImplementedError()
    
    def Imul(self, data, init=None, reset=None):
        raise NotImplementedError()
    
    def Idiv(self, data, init=None, reset=None):
        raise NotImplementedError()
    
    def Icustom(self, data, init=None, reset=None):
        raise NotImplementedError()