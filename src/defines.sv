

package defines;
    typedef enum logic [3:0] {ADD, SUBTRACT, LESS_THAN, LESS_THAN_UNSIGNED, AND, OR, XOR, SHIFT_LEFT, SHIFT_RIGHT_LOGICAL, SHIFT_RIGHT_ARITHMETIC } alu_operation_t;
    typedef enum logic [1:0] { RS1, RS2, IMM, PC } alu_operand_t;
endpackage