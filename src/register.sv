
module register # (
  parameter SIZE = 32
)
(
  input clk,
  input rst,
  input load_en,

  input [SIZE-1:0] d,

  output reg [SIZE-1:0] q
);
  
  always @(posedge clk, posedge rst) begin
    if (rst) begin
      q <= 0;
    end else begin
      if (load_en)
        q <= d;
    end
  end

endmodule
