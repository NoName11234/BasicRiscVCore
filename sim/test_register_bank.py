# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge, NextTimeStep, Timer
from cocotb.types import LogicArray
from cocotb.handle import Force

@cocotb.test()
async def register_bank_write_test(dut):
    dut.rst.value = 1
    dut.load_en.value = 1
    dut.data_in.value = 0
    dut.sel_in.value = 0

    await Timer(1, "ns")
    dut.rst.value = 0

    clock = Clock(dut.clk, 10, "ns")
    cocotb.start_soon(clock.start(start_high=False))

    # write random data to random register and check

    for i in range(10):
        data = random.randrange(2**32)
        sel = random.randrange(1, 32) # reg0 is rardwired to 0
        dut.sel_in.value = sel
        dut.data_in.value = data

        await RisingEdge(dut.clk)
        await NextTimeStep()

        assert dut.x[sel].q.value == data, f"data {data} does not match register {sel}: contains {dut.x[sel].q.value}"




@cocotb.test()
async def register_bank_read_test(dut):
    dut.rst.value = 0
    dut.load_en.value = 0
    dut.data_in.value = 0
    dut.sel_in.value = 0

    for i in range(10):
        data_a = random.randrange(2**32)
        data_b = random.randrange(2**32)
        sel = random.sample(range(1,32), k=2) # chooses two unique registers from 1..31
        sel_a = sel[0]
        sel_b = sel[1]
        
        dut.x[sel_a].q.value = data_a # set data into the registers
        dut.x[sel_b].q.value = data_b
        dut.sel_out_a.value = sel_a
        dut.sel_out_b.value = sel_b

        await Timer(1, "ns")

        assert dut.data_out_a.value == data_a
        assert dut.data_out_b.value == data_b
    

    # check for hard wired x0
    dut.sel_out_a.value = 0
    dut.sel_out_b.value = 0

    await Timer(1, "ns")
    
    assert dut.data_out_a.value == 0
    assert dut.data_out_b.value == 0
    



@cocotb.test()
async def register_bank_reset_test(dut):
    dut.rst.value = 0
    dut.load_en.value = 0
    dut.data_in.value = 0
    dut.sel_in.value = 0

    data = random.choices(range(2**32), k=31)
    for reg in range(1, 32):
        dut.x[reg].reg_instance.q.value = data[reg - 1]

    await Timer(1, "ns")
    dut.rst.value = 1
    await Timer(1, "ns")

    for reg in range(1, 32):
        dut._log.info("reset of reg %d is %d", reg, dut.x[reg].reg_instance.rst.value)
        dut._log.info("q of reg %d is %d", reg, dut.x[reg].reg_instance.q.value)
        assert dut.x[reg].q.value == 0, f"register {reg} was not reset correctly"


def test_register_bank_runner():

    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    src_path = proj_path / "src"
    verilog_sources = [src_path / "register.sv", src_path / "register_bank.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="register_bank",
        always=True,
        timescale=("1ns","1ps")
    )

    runner.test(hdl_toplevel="register_bank", test_module="test_register_bank,", timescale=("1ns","1ps"))


if __name__ == "__main__":
    test_register_bank_runner()