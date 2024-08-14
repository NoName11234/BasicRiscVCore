"""
This file contains global definitions that reflect the SystemVerilog definitions in `src/defines.sv`
"""
from enum import IntEnum


class AluOperation(IntEnum):
    """
    This enum defines the opcodes from src/defines.sv for the python test code
    """
    ADD                     = 0
    SUBTRACT                = 1
    LESS_THAN               = 2
    LESS_THAN_UNSIGNED      = 3 
    AND                     = 4
    OR                      = 5
    XOR                     = 6
    SHIFT_LEFT              = 7
    SHIFT_RIGHT_LOGICAL     = 8
    SHIFT_RIGHT_ARITHMETIC  = 9

class AluOperand(IntEnum):
    """
    This enum defines the operands from src/defines.sv for the python test code
    """
    RS1 = 0
    RS2 = 1
    IMM = 2
    PC = 3
