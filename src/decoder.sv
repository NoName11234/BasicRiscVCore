module decoder import defines::*(
    input [31:0] instruction,

    //alu outputs
    output reg [31:0] alu_immediate,
    output alu_operand_t operand_a,
    output alu_operand_t operand_b,
    output alu_operation_t operation,

    //program counter outputs
    output pc_load_enable,
    output pc_count_enable,
    output pc_preset_value,

    //mainbus
    output mainbus_alu_select,
    output mainbus_register_bank_select,
    output mainbus_memory_select,

    //register bank
    output bank_load_enable,
    output reg [4:0] bank_select_in,
    output reg [4:0] bank_select_out_a,
    output reg [4:0] bank_select_out_b
);

endmodule