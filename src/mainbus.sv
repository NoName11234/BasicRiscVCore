module mainbus (
    input alu,
    input register_bank,
    input memory,

    input [31:0] alu_in,
    input [31:0] register_bank_in,
    input [31:0] memory_in,

    output reg [31:0] data_out
);

    always @(*) begin
        if(alu) begin
            data_out = alu_in;
        end else if(register_bank) begin
            data_out = register_bank_in;
        end else if(memory) begin
            data_out = memory_in;
        end else begin
            data_out = 0;
        end
    end

endmodule