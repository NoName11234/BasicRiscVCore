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

    always_comb begin
        // defaults
        alu_immediate = 32'd0;
        operand_a = defines::RS1;
        operand_b = defines::IMM;
        operation = defines::ADD; // ADD
        pc_load_enable = 1'h0;
        pc_count_enable = 1'b1;
        pc_preset_value = 32'd0;
        mainbus_alu_select = 0;
        mainbus_register_bank_select = 0;
        mainbus_memory_select = 0;
        bank_load_enable = 0;
        bank_select_in = 5'd0;
        bank_select_out_a = 5'd0;
        bank_select_out_b = 5'd0;


        casez (instruction)
            // instruction encoding type R
            riscv_instr::ADD: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
                operation = defines::ADD;
            end 
            riscv_instr::SUB: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
                operation = defines::SUBTRACT;
            end 
            riscv_instr::SLL: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
                operation = defines::SHIFT_LEFT;
            end 
            riscv_instr::SLT: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
                operation = defines::LESS_THAN;
            end 
            riscv_instr::SLTU: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::XOR: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::SRL: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::SRA: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::OR: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::AND: begin
                mainbus_alu_select = 1;
                bank_select_in = instruction[11:7];
                bank_load_enable = 1;
                bank_select_out_a = instruction[19:15];
                bank_select_out_b = instruction[24:20];
                operand_a = RS1;
                operand_b = RS2;
            end 
            riscv_instr::LB, riscv_instr::LH, riscv_instr::LW, riscv_instr::LBU, riscv_instr::LHU, riscv_instr::ADDI, riscv_instr::SLTI, riscv_instr::SLTIU, riscv_instr::XORI, riscv_instr::ORI, riscv_instr::ANDI, riscv_instr::SLLI, riscv_instr::SRLI, riscv_instr::SRAI: begin
                // instruction encoding type I
            end
            riscv_instr::SB, riscv_instr::SH, riscv_instr::SW: begin
                // instruction encoding type S
            end
            riscv_instr::BEQ, riscv_instr::BNE, riscv_instr::BLT, riscv_instr::BGE, riscv_instr::BLTU, riscv_instr::BGEU: begin
                // instruction encoding type B
            end
            riscv_instr::LUI, riscv_instr::AUIPC: begin
                // instruction encoding type U
            end
            riscv_instr::ECALL: begin

            end
            riscv_instr::EBREAK: begin
                
            end

            default: 
        endcase
    end


endmodule