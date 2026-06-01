`default_nettype none

module tt_um_cambridge_nlfsr (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (1=out, 0=in)
    input  wire       ena,      // always 1
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // 16-bit internal state for better complexity
    reg [15:0] n_reg;
    
    // ui_in[0] is our "Program" switch
    wire mode = ui_in[0]; 
    wire feedback;

    // Function 1: Algebraic complexity using AND/XOR
    // f = x^16 + x^14 + x^13 + x^11 + (x^3 & x^1)
    wire func_a = n_reg[15] ^ n_reg[13] ^ n_reg[12] ^ (n_reg[2] & n_reg[0]);

    // Function 2: "Chaotic" variant with different taps
    // f = x^16 + x^12 + x^9 + (x^7 | x^4)
    wire func_b = n_reg[15] ^ n_reg[11] ^ (n_reg[6] | n_reg[3]);

    assign feedback = mode ? func_b : func_a;

    always @(posedge clk) begin
        if (!rst_n) begin
            n_reg <= 16'hACE1; // Non-zero seed
        end else begin
            // Shift and inject feedback with a "zero-trap" protector
            n_reg <= {n_reg[14:0], feedback ^ (n_reg == 16'h0000)};
        end
    end

    // Output the top 8 bits to the dedicated pins
    assign uo_out  = n_reg[15:8];
    // Output the lower 8 bits to the bidirectional pins
    assign uio_out = n_reg[7:0];
    assign uio_oe  = 8'b11111111; // Configure all UIO as outputs

endmodule
