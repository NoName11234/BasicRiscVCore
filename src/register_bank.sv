
module register_bank
(
  input clk,
  input rst,

  input [31:0] data_in,
  input [4:0] sel_in,
  input load_en,

  output reg [31:0] data_out_a,
  input [4:0] sel_out_a,

  output reg [31:0] data_out_b,
  input [4:0] sel_out_b
);
  genvar i;

  generate
    for (i = 1; i < 32; i = i+1) begin: x
        wire [31:0] q;
        register #(.SIZE(32)) reg_instance (
            .clk(clk),
            .rst(rst),
            .load_en(load_en && (sel_in == i)),
            .d(data_in),
            .q(q)
        );
    end
  endgenerate

  always @(*) begin
    case (sel_out_a)
        5'd00: data_out_a = 32'd0;
        5'd01: data_out_a = x[01].q;
        5'd02: data_out_a = x[02].q;
        5'd03: data_out_a = x[03].q;
        5'd04: data_out_a = x[04].q;
        5'd05: data_out_a = x[05].q;
        5'd06: data_out_a = x[06].q;
        5'd07: data_out_a = x[07].q;
        5'd08: data_out_a = x[08].q;
        5'd09: data_out_a = x[09].q;
        5'd10: data_out_a = x[10].q;
        5'd11: data_out_a = x[11].q;
        5'd12: data_out_a = x[12].q;
        5'd13: data_out_a = x[13].q;
        5'd14: data_out_a = x[14].q;
        5'd15: data_out_a = x[15].q;
        5'd16: data_out_a = x[16].q;
        5'd17: data_out_a = x[17].q;
        5'd18: data_out_a = x[18].q;
        5'd19: data_out_a = x[19].q;
        5'd20: data_out_a = x[20].q;
        5'd21: data_out_a = x[21].q;
        5'd22: data_out_a = x[22].q;
        5'd23: data_out_a = x[23].q;
        5'd24: data_out_a = x[24].q;
        5'd25: data_out_a = x[25].q;
        5'd26: data_out_a = x[26].q;
        5'd27: data_out_a = x[27].q;
        5'd28: data_out_a = x[28].q;
        5'd29: data_out_a = x[29].q;
        5'd30: data_out_a = x[30].q;
        5'd31: data_out_a = x[31].q;
    endcase
  end

  always @(*) begin
    case (sel_out_b)
        5'd00: data_out_b = 32'd0;
        5'd01: data_out_b = x[01].q;
        5'd02: data_out_b = x[02].q;
        5'd03: data_out_b = x[03].q;
        5'd04: data_out_b = x[04].q;
        5'd05: data_out_b = x[05].q;
        5'd06: data_out_b = x[06].q;
        5'd07: data_out_b = x[07].q;
        5'd08: data_out_b = x[08].q;
        5'd09: data_out_b = x[09].q;
        5'd10: data_out_b = x[10].q;
        5'd11: data_out_b = x[11].q;
        5'd12: data_out_b = x[12].q;
        5'd13: data_out_b = x[13].q;
        5'd14: data_out_b = x[14].q;
        5'd15: data_out_b = x[15].q;
        5'd16: data_out_b = x[16].q;
        5'd17: data_out_b = x[17].q;
        5'd18: data_out_b = x[18].q;
        5'd19: data_out_b = x[19].q;
        5'd20: data_out_b = x[20].q;
        5'd21: data_out_b = x[21].q;
        5'd22: data_out_b = x[22].q;
        5'd23: data_out_b = x[23].q;
        5'd24: data_out_b = x[24].q;
        5'd25: data_out_b = x[25].q;
        5'd26: data_out_b = x[26].q;
        5'd27: data_out_b = x[27].q;
        5'd28: data_out_b = x[28].q;
        5'd29: data_out_b = x[29].q;
        5'd30: data_out_b = x[30].q;
        5'd31: data_out_b = x[31].q;
    endcase
  end

endmodule