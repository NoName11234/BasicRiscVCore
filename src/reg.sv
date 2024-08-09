`timescale 1ns/1ps

module register # (
  parameter SIZE = 32
)
(
  input [SIZE-1:0] d,
  input clk,
  input rst,
  output reg [SIZE-1:0] q
);
  
  always @(posedge clk, posedge rst) begin
    if (rst) begin
      q <= 0;
    end else begin
      q <= d;
    end
  end

endmodule
