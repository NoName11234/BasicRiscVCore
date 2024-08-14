
module alu import defines::*; (
    // possible operands
    input [31:0] rs1,
    input [31:0] rs2,
    input [31:0] imm,
    input [31:0] pc,

    // control signals
    input alu_operand_t operand_a_select,
    input alu_operand_t operand_b_select,
    input alu_operation_t operation,

    // result
    output reg [31:0] result
);

    reg [31:0] operand_a;
    reg [31:0] operand_b;

    always_comb begin
        case (operand_a_select)
            RS1: operand_a = rs1; 
            RS2: operand_a = rs2; 
            IMM: operand_a = imm; 
            PC:  operand_a = pc;
        endcase
    end

    always_comb begin
        case (operand_b_select)
            RS1: operand_b = rs1; 
            RS2: operand_b = rs2; 
            IMM: operand_b = imm; 
            PC:  operand_b = pc;
        endcase
    end

    always_comb begin
        case (operation)
            ADD:                    result[31:0] = operand_a            +       operand_b;
            SUBTRACT:               result[31:0] = operand_a            -       operand_b;
            LESS_THAN:              result[31:0] = $signed(operand_a)   <       $signed(operand_b);
            LESS_THAN_UNSIGNED:     result[31:0] = $unsigned(operand_a) <       $unsigned(operand_b);
            AND:                    result[31:0] = operand_a            &       operand_b;
            OR:                     result[31:0] = operand_a            |       operand_b;
            XOR:                    result[31:0] = operand_a            ^       operand_b;
            SHIFT_LEFT:             result[31:0] = operand_a            <<      operand_b;
            SHIFT_RIGHT_LOGICAL:    result[31:0] = operand_a            >>      operand_b;
            SHIFT_RIGHT_ARITHMETIC: result[31:0] = $signed(operand_a)   >>>     operand_b;
        endcase
    end


endmodule