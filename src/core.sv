

module core (
    input clk,
    input rst
);
    
    wire [31:0] data_bus;
    
    // program counter (pc) connections
    wire pc_load_en;
    wire [31:0] pc_data_out;

    // register bank connections
    wire reg_bank_load_en;
    wire [31:0] reg_bank_data_out_a;
    wire [31:0] reg_bank_data_out_b;
    wire [4:0] reg_bank_sel_in;
    wire [4:0] reg_bank_sel_out_a;
    wire [4:0] reg_bank_sel_out_b;


    register_bank reg_bank (
        .clk(clk),
        .rst(rst),
        .data_in(data_bus),
        .sel_in(reg_bank_sel_in),
        .load_en(reg_bank_load_en),
        .data_out_a(reg_bank_data_out_a),
        .sel_out_a(reg_bank_sel_out_a),
        .data_out_b(reg_bank_data_out_b),
        .sel_out_b(reg_bank_sel_out_b)
    );

    register #(.SIZE(32)) pc (
        .clk(clk),
        .rst(rst),
        .load_en(pc_load_en),
        .d(data_bus),
        .q(pc_data_out)
    );


endmodule