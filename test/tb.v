`default_nettype none
`timescale 1ns / 1ps

/* TinyTapeout Testbench for Programmable NLFSR
   Note: Library includes (primitives.v, etc.) are handled via 
   the Makefile COMPILE_ARGS to ensure compatibility with 
   the GitHub Action environment.
*/

module tb ();

  // Dump the signals to a FST file for GTKWave/Surfer
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate the NLFSR module
  tt_um_cambridge_nlfsr user_project (

`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path
      .ena    (ena),      // enable
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // reset_n (active low)
  );

endmodule
