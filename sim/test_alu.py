# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import itertools

import cocotb
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import NextTimeStep, Timer, ReadOnly
from cocotb.types import LogicArray
from cocotb.handle import Force

from defines import AluOperation, AluOperand

@cocotb.test()
async def alu_test_operations(dut):
    """
    Tests the operations of the alu
    """

    # set presets
    dut.rs1.value = 0
    dut.rs2.value = 0
    dut.imm.value = 0
    dut.pc.value = 0

    dut.operand_a_select.value = AluOperand.RS1
    dut.operand_b_select.value = AluOperand.RS2
    dut.operation.value = AluOperation.ADD

    await Timer(1,"ns")

    assert dut.result.value == 0, f"result not initialized correctly (expected 0, got {dut.result.value})"

    dut._log.info("performing ADD")
    for _ in range(100):
        dut.operation.value = AluOperation.ADD
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert (int(dut.rs1.value) + int(dut.rs2.value)) & 0xffffffff == int(dut.result.value)

    dut._log.info("performing SUBTRACT")
    for _ in range(100):
        dut.operation.value = AluOperation.SUBTRACT
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert (int(dut.rs1.value) - int(dut.rs2.value)) & 0xffffffff == int(dut.result.value)

    dut._log.info("performing LESS_THAN")
    for _ in range(100):
        dut.operation.value = AluOperation.LESS_THAN
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert int(dut.result.value) == (1 if dut.rs1.value.signed_integer < dut.rs2.value.signed_integer else 0) 
        
    dut._log.info("performing LESS_THAN_UNSIGNED")
    for _ in range(100):
        dut.operation.value = AluOperation.LESS_THAN_UNSIGNED
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert int(dut.result.value) == (1 if dut.rs1.value.integer < dut.rs2.value.integer else 0)  
        
    dut._log.info("performing AND")
    for _ in range(100):
        dut.operation.value = AluOperation.AND
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert dut.result.value == dut.rs1.value & dut.rs2.value
    
    dut._log.info("performing OR")
    for _ in range(100):
        dut.operation.value = AluOperation.OR
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert dut.result.value == dut.rs1.value | dut.rs2.value
    
    dut._log.info("performing XOR")
    for _ in range(100):
        dut.operation.value = AluOperation.XOR
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**32)
        await Timer(1,"ns")
        assert dut.result.value == dut.rs1.value ^ dut.rs2.value

    dut._log.info("performing SHIFT_LEFT")
    for _ in range(100):
        dut.operation.value = AluOperation.SHIFT_LEFT 
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**5)
        await Timer(1,"ns")
        assert dut.result.value == (dut.rs1.value << dut.rs2.value) & 0xffffffff

    dut._log.info("performing SHIFT_RIGHT_LOGICAL")
    for _ in range(100):
        dut.operation.value = AluOperation.SHIFT_RIGHT_LOGICAL 
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**5)
        await Timer(1,"ns")
        assert dut.result.value == (dut.rs1.value >> dut.rs2.value) & 0xffffffff
    
    dut._log.info("performing SHIFT_RIGHT_ARITHMETIC")
    for _ in range(100):
        dut.operation.value = AluOperation.SHIFT_RIGHT_ARITHMETIC 
        dut.rs1.value = random.randrange(2**32)
        dut.rs2.value = random.randrange(2**5)
        await Timer(1,"ns")
        assert dut.result.value == (dut.rs1.value.signed_integer >> dut.rs2.value) & 0xffffffff

@cocotb.test()
async def alu_test_operands(dut):
    # set presets
    dut.rs1.value = 0
    dut.rs2.value = 0
    dut.imm.value = 0
    dut.pc.value = 0

    dut.operand_a_select.value = AluOperand.RS1
    dut.operand_b_select.value = AluOperand.RS2
    dut.operation.value = AluOperation.ADD

    await Timer(1,"ns")

    assert dut.result.value == 0
    

    # iterate over all combinations without doubles: no (rs1, rs1), (rs2, rs2), ...
    for opA, opB in itertools.permutations(AluOperand, 2):
        dut.operand_a_select.value = opA
        dut.operand_b_select.value = opB

        op1 = random.randrange(2**32)
        op2 = random.randrange(2**32)
        
        getattr(dut, opA.name.lower()).value = op1
        getattr(dut, opB.name.lower()).value = op2

        await Timer(1,"ns")
        assert dut.operand_a.value.integer == op1
        assert dut.operand_b.value.integer == op2

    for op in AluOperand:
        dut.operand_a_select.value = op
        dut.operand_b_select.value = op

        data = random.randrange(2**32)
        
        getattr(dut, op.name.lower()).value = data

        await Timer(1,"ns")
        assert dut.operand_a.value.integer == data
        assert dut.operand_b.value.integer == data

def test_alu_runner():
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    src_path = proj_path / "src"
    verilog_sources = [src_path / "defines.sv", src_path / "alu.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="alu",
        always=True,
        timescale=("1ns","1ps")
    )

    runner.test(hdl_toplevel="alu", test_module="test_alu,", timescale=("1ns","1ps"))


if __name__ == "__main__":
    test_alu_runner()