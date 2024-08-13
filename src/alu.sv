typedef enum {ADD,  } alu_operation_t;
typedef enum {}

module alu (
    // possible operands
    input [31:0] rs1;
    input [31:0] rs2;
    input [31:0] imm;
    input [31:0] pc;





    // result
    output reg [31:0] result; 
);

endmodule