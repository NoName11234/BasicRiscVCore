
module counter # (
  parameter SIZE = 32
)
(
  input clk,
  input rst,
  input load_en,
  input count_en,

  input [SIZE-1:0] preset_value,

  output reg [SIZE-1:0] counter_value
);
  
  always @(posedge clk, posedge rst) begin
    if (rst) begin
      counter_value <= 0;
    end else begin
      if (load_en)
        counter_value <= preset_value;
      else if (count_en)
        counter_value <= counter_value + 1;
    end
  end

endmodule
