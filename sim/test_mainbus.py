import os
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer

@cocotb.test()
async def mainbus_test_alu_input(dut):
    """
    Tests whether input from alu is passed through
    """

    dut.alu.value = 1
    dut.register_bank.value = 0
    dut.memory.value = 0

    dut.alu_in.value = 5
    dut.register_bank_in.value = 10
    dut.memory_in.value = 20

    await Timer(1,"ns")

    assert dut.data_out.value == 5, f"alu_in is not passed through to data_out"

@cocotb.test()
async def mainbus_test_register_bank_input(dut):
    """
    Tests whether input from register bank is passed through
    """
    dut.alu.value = 0
    dut.register_bank.value = 1
    dut.memory.value = 0

    dut.alu_in.value = 5
    dut.register_bank_in.value = 10
    dut.memory_in.value = 20

    await Timer(1,"ns")

    assert dut.data_out.value == 10, f"register_bank_in is not passed through to data_out"

@cocotb.test()
async def mainbus_test_memory_input(dut):
    """
    Tests whether input from decoder is passed through
    """
    dut.alu.value = 0
    dut.register_bank.value = 0
    dut.memory.value = 1

    dut.alu_in.value = 5
    dut.register_bank_in.value = 10
    dut.memory_in.value = 20

    await Timer(1,"ns")

    assert dut.data_out.value == 20, f"memory_in is not passed through to data_out"

@cocotb.test()
async def mainbus_test_no_input(dut):
    """
    Tests whether input from decoder is passed through
    """
    dut.alu.value = 0
    dut.register_bank.value = 0
    dut.memory.value = 0

    dut.alu_in.value = 5
    dut.register_bank_in.value = 10
    dut.memory_in.value = 20

    await Timer(1,"ns")

    assert dut.data_out.value == 0, f"data_out is not set to zero when no input is selected"

def test_mainbus_runner():
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    src_path = proj_path / "src"
    verilog_sources = [src_path / "mainbus.sv"]

    runner = get_runner(sim)

    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="mainbus",
        always=True,
        timescale=("1ns","1ps")
    )

    runner.test(hdl_toplevel="mainbus", test_module="test_mainbus,", timescale=("1ns","1ps"))


if __name__=="__main__":
    test_mainbus_runner()