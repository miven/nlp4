 /*                                                                      
 Copyright 2019 Blue Liang, liangkangnan@163.com
                                                                         
 Licensed under the Apache License, Version 2.0 (the "License");         
 you may not use this file except in compliance with the License.        
 You may obtain a copy of the License at                                 
                                                                         
     http://www.apache.org/licenses/LICENSE-2.0                          
                                                                         
 Unless required by applicable law or agreed to in writing, software    
 distributed under the License is distributed on an "AS IS" BASIS,       
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and     
 limitations under the License.                                          
 */

`include "defines.v"

// excute and writeback module
module ex (

    input wire clk,
    input wire rst,

    // from id
    input wire[`SramBus] inst_i,            // inst content
    input wire inst_valid_i,
    input wire[`SramAddrBus] inst_addr_i,   // inst addr
    input wire reg_we_i,
    input wire[`RegAddrBus] reg_waddr_i,

    // from regs
    input wire[`RegBus] reg1_rdata_i,       // reg1 read data
    input wire[`RegBus] reg2_rdata_i,       // reg2 read data

    // from sram
    input wire[`SramBus] sram_rdata_i,      // ram read data

    // from div
    input wire div_ready_i,
    input wire[`DoubleRegBus] div_result_i,

    // to sram
    output reg[`SramBus] sram_wdata_o,      // ram write data
    output reg[`SramAddrBus] sram_raddr_o,  // ram read addr
    output reg[`SramAddrBus] sram_waddr_o,  // ram write addr

    // to regs
    output reg[`RegBus] reg_wdata_o,        // reg write data
    output reg reg_we_o,                    // reg write enable
    output reg[`RegAddrBus] reg_waddr_o,    // reg write addr

    // to div
    output reg[`RegBus] div_dividend_o,
    output reg[`RegBus] div_divisor_o,
    output reg div_start_o,

    // to pc_reg
    output reg hold_flag_o,
    output reg[`RegBus] hold_addr_o,

    // to pc_reg
    output reg jump_flag_o,                // if jump or not flag
    output reg[`RegBus] jump_addr_o        // jump dest addr

);

    wire[31:0] sign_extend_tmp;
    wire[4:0] shift_bits;
    reg[1:0] sram_raddr_index;
    reg[1:0] sram_waddr_index;
    wire[`DoubleRegBus] mul_temp;
    wire[`DoubleRegBus] mulh_temp;
    wire[`DoubleRegBus] mulh_temp_invert;
    wire[`DoubleRegBus] mulhsu_temp;
    wire[`DoubleRegBus] mulhsu_temp_invert;
    wire[`RegBus] op1_mul;
    wire[`RegBus] op2_mul;
    reg div_starting;
    reg is_jumping;
    reg div_reg_we;
    reg[4:0] div_rd_reg;
    reg[2:0] div_funct3;

    wire[6:0] opcode = inst_i[6:0];
    wire[2:0] funct3 = inst_i[14:12];
    wire[6:0] funct7 = inst_i[31:25];
    wire[4:0] rd = inst_i[11:7];

    assign sign_extend_tmp = {{20{inst_i[31]}}, inst_i[31:20]};
    assign shift_bits = inst_i[24:20];
    assign mul_temp = reg1_rdata_i * reg2_rdata_i;
    assign op1_mul = (reg1_rdata_i[31] == 1'b1)? (~reg1_rdata_i + 1): reg1_rdata_i;
    assign op2_mul = (reg2_rdata_i[31] == 1'b1)? (~reg2_rdata_i + 1): reg2_rdata_i;
    assign mulhsu_temp = op1_mul * reg2_rdata_i;
    assign mulh_temp = op1_mul * op2_mul;
    assign mulhsu_temp_invert = ~mulhsu_temp + 1;
    assign mulh_temp_invert = ~mulh_temp + 1;


    always @ (posedge clk) begin
        if (rst == `RstEnable) begin
            sram_raddr_o <= `ZeroWord;
            jump_flag_o <= `JumpDisable;
            hold_flag_o <= `HoldDisable;
            sram_raddr_index <= 2'b0;
            sram_waddr_index <= 2'b0;
            div_starting <= `DivStop;
            is_jumping <= `False;
            div_reg_we <= `WriteDisable;
            div_start_o <= `DivStop;
        end
    end

    always @ (*) begin
        div_dividend_o <= reg1_rdata_i;
        div_divisor_o <= reg2_rdata_i;
    end

    always @ (*) begin
        reg_we_o <= reg_we_i | div_reg_we;
    end

    always @ (*) begin
        if ((is_jumping == `False) && (div_starting == `DivStart)) begin
            if (div_ready_i == `DivResultReady) begin
                case (div_funct3)
                    `INST_DIV: begin
                        div_reg_we <= `WriteEnable;
                        reg_waddr_o <= div_rd_reg;
                        reg_wdata_o <= div_result_i[31:0];
                        div_starting <= `DivStop;
                        div_start_o <= `DivStop;
                        hold_flag_o <= `HoldDisable;
                    end
                    `INST_DIVU: begin
                        div_reg_we <= `WriteEnable;
                        reg_waddr_o <= div_rd_reg;
                        reg_wdata_o <= div_result_i[31:0];
                        div_starting <= `DivStop;
                        div_start_o <= `DivStop;
                        hold_flag_o <= `HoldDisable;
                    end
                    `INST_REM: begin
                        div_reg_we <= `WriteEnable;
                        reg_waddr_o <= div_rd_reg;
                        reg_wdata_o <= div_result_i[63:32];
                        div_starting <= `DivStop;
                        div_start_o <= `DivStop;
                        hold_flag_o <= `HoldDisable;
                    end
                    `INST_REMU: begin
                        div_reg_we <= `WriteEnable;
                        reg_waddr_o <= div_rd_reg;
                        reg_wdata_o <= div_result_i[63:32];
                        div_starting <= `DivStop;
                        div_start_o <= `DivStop;
                        hold_flag_o <= `HoldDisable;
                    end
                endcase
            end
        end else if (inst_valid_i == `InstValid) begin
            div_reg_we <= `WriteDisable;
            reg_waddr_o <= reg_waddr_i;
            case (opcode)
                `INST_TYPE_I: begin
                    case (funct3)
                        `INST_ADDI: begin
                            jump_flag_o <= `JumpDisable;
                            reg_wdata_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                        end
                        `INST_SLTI: begin
                            jump_flag_o <= `JumpDisable;
                            if (reg1_rdata_i[31] == 1'b1 && sign_extend_tmp[31] == 1'b1) begin
                                if (reg1_rdata_i < sign_extend_tmp) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else begin
                                    reg_wdata_o <= 32'h00000000;
                                end
                            end else if (reg1_rdata_i[31] == 1'b1 && sign_extend_tmp[31] == 1'b0) begin
                                reg_wdata_o <= 32'h00000001;
                            end else if (reg1_rdata_i[31] == 1'b0 && sign_extend_tmp[31] == 1'b1) begin
                                reg_wdata_o <= 32'h00000000;
                            end else begin
                                if (reg1_rdata_i < sign_extend_tmp) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else begin
                                    reg_wdata_o <= 32'h00000000;
                                end
                            end
                        end
                        `INST_SLTIU: begin
                            jump_flag_o <= `JumpDisable;
                            if (reg1_rdata_i[31] == 1'b1 && sign_extend_tmp[31] == 1'b1) begin
                                if (reg1_rdata_i < sign_extend_tmp) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else begin
                                    reg_wdata_o <= 32'h00000000;
                                end
                            end else if (reg1_rdata_i[31] == 1'b1 && sign_extend_tmp[31] == 1'b0) begin
                                reg_wdata_o <= 32'h00000000;
                            end else if (reg1_rdata_i[31] == 1'b0 && sign_extend_tmp[31] == 1'b1) begin
                                reg_wdata_o <= 32'h00000001;
                            end else begin
                                if (reg1_rdata_i < sign_extend_tmp) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else begin
                                    reg_wdata_o <= 32'h00000000;
                                end
                            end
                        end
                        `INST_XORI: begin
                            jump_flag_o <= `JumpDisable;
                            reg_wdata_o <= reg1_rdata_i ^ {{20{inst_i[31]}}, inst_i[31:20]};
                        end
                        `INST_ORI: begin
                            jump_flag_o <= `JumpDisable;
                            reg_wdata_o <= reg1_rdata_i | {{20{inst_i[31]}}, inst_i[31:20]};
                        end
                        `INST_ANDI: begin
                            jump_flag_o <= `JumpDisable;
                            reg_wdata_o <= reg1_rdata_i & {{20{inst_i[31]}}, inst_i[31:20]};
                        end
                        `INST_SLLI: begin
                            jump_flag_o <= `JumpDisable;
                            reg_wdata_o <= reg1_rdata_i << shift_bits;
                        end
                        `INST_SRI: begin
                            jump_flag_o <= `JumpDisable;
                            if (inst_i[30] == 1'b1) begin
                                reg_wdata_o <= ({32{reg1_rdata_i[31]}} << (6'd32 - {1'b0, shift_bits})) | (reg1_rdata_i >> shift_bits);
                            end else begin
                                reg_wdata_o <= reg1_rdata_i >> shift_bits;
                            end
                        end
                    endcase
                end
                `INST_TYPE_R_M: begin
                    if ((funct7 == 7'b0000000) || (funct7 == 7'b0100000)) begin
                        case (funct3)
                            `INST_ADD_SUB: begin
                                jump_flag_o <= `JumpDisable;
                                if (inst_i[30] == 1'b0) begin
                                    reg_wdata_o <= reg1_rdata_i + reg2_rdata_i;
                                end else begin
                                    reg_wdata_o <= reg1_rdata_i - reg2_rdata_i;
                                end
                            end
                            `INST_SLL: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= reg1_rdata_i << reg2_rdata_i[4:0];
                            end
                            `INST_SLT: begin
                                jump_flag_o <= `JumpDisable;
                                if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                    if (reg1_rdata_i < reg2_rdata_i) begin
                                        reg_wdata_o <= 32'h00000001;
                                    end else begin
                                        reg_wdata_o <= 32'h00000000;
                                    end
                                end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b0) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b1) begin
                                    reg_wdata_o <= 32'h00000000;
                                end else begin
                                    if (reg1_rdata_i < reg2_rdata_i) begin
                                        reg_wdata_o <= 32'h00000001;
                                    end else begin
                                        reg_wdata_o <= 32'h00000000;
                                    end
                                end
                            end
                            `INST_SLTU: begin
                                jump_flag_o <= `JumpDisable;
                                if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                    if (reg1_rdata_i < reg2_rdata_i) begin
                                        reg_wdata_o <= 32'h00000001;
                                    end else begin
                                        reg_wdata_o <= 32'h00000000;
                                    end
                                end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b0) begin
                                    reg_wdata_o <= 32'h00000000;
                                end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b1) begin
                                    reg_wdata_o <= 32'h00000001;
                                end else begin
                                    if (reg1_rdata_i < reg2_rdata_i) begin
                                        reg_wdata_o <= 32'h00000001;
                                    end else begin
                                        reg_wdata_o <= 32'h00000000;
                                    end
                                end
                            end
                            `INST_XOR: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= reg1_rdata_i ^ reg2_rdata_i;
                            end
                            `INST_SR: begin
                                jump_flag_o <= `JumpDisable;
                                if (inst_i[30] == 1'b1) begin
                                    reg_wdata_o <= ({32{reg1_rdata_i[31]}} << (6'd32 - {1'b0, reg2_rdata_i[4:0]})) | (reg1_rdata_i >> reg2_rdata_i[4:0]);
                                end else begin
                                    reg_wdata_o <= reg1_rdata_i >> reg2_rdata_i[4:0];
                                end
                            end
                            `INST_OR: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= reg1_rdata_i | reg2_rdata_i;
                            end
                            `INST_AND: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= reg1_rdata_i & reg2_rdata_i;
                            end
                        endcase
                    end else if (funct7 == 7'b0000001) begin
                        case (funct3)
                            `INST_MUL: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= mul_temp[31:0];
                            end
                            `INST_MULHU: begin
                                jump_flag_o <= `JumpDisable;
                                reg_wdata_o <= mul_temp[63:32];
                            end
                            `INST_MULH: begin
                                jump_flag_o <= `JumpDisable;
                                if ((reg1_rdata_i[31] == 1'b0) && (reg2_rdata_i[31] == 1'b0)) begin
                                    reg_wdata_o <= mulh_temp[63:32];
                                end else if ((reg1_rdata_i[31] == 1'b1) && (reg2_rdata_i[31] == 1'b1)) begin
                                    reg_wdata_o <= mulh_temp[63:32];
                                end else if ((reg1_rdata_i[31] == 1'b1) && (reg2_rdata_i[31] == 1'b0)) begin
                                    reg_wdata_o <= mulh_temp_invert[63:32];
                                end else begin
                                    reg_wdata_o <= mulh_temp_invert[63:32];
                                end
                            end
                            `INST_MULHSU: begin
                                jump_flag_o <= `JumpDisable;
                                if (reg1_rdata_i[31] == 1'b1) begin
                                    reg_wdata_o <= mulhsu_temp_invert[63:32];
                                end else begin
                                    reg_wdata_o <= mulhsu_temp[63:32];
                                end
                            end
                            `INST_DIV: begin
                                jump_flag_o <= `JumpDisable;
                                hold_flag_o <= `HoldEnable;
                                div_start_o <= `DivStart;
                                div_starting <= `DivStart;
                                div_rd_reg <= rd;
                                div_funct3 <= funct3;
                                hold_addr_o <= inst_addr_i + 4'h4;
                            end
                            `INST_DIVU: begin
                                jump_flag_o <= `JumpDisable;
                                hold_flag_o <= `HoldEnable;
                                div_start_o <= `DivStart;
                                div_starting <= `DivStart;
                                div_rd_reg <= rd;
                                div_funct3 <= funct3;
                                hold_addr_o <= inst_addr_i + 4'h4;
                            end
                            `INST_REM: begin
                                jump_flag_o <= `JumpDisable;
                                hold_flag_o <= `HoldEnable;
                                div_start_o <= `DivStart;
                                div_starting <= `DivStart;
                                div_rd_reg <= rd;
                                div_funct3 <= funct3;
                                hold_addr_o <= inst_addr_i + 4'h4;
                            end
                            `INST_REMU: begin
                                jump_flag_o <= `JumpDisable;
                                hold_flag_o <= `HoldEnable;
                                div_start_o <= `DivStart;
                                div_starting <= `DivStart;
                                div_rd_reg <= rd;
                                div_funct3 <= funct3;
                                hold_addr_o <= inst_addr_i + 4'h4;
                            end
                        endcase
                    end
                end
                `INST_TYPE_L: begin
                    case (funct3)
                        `INST_LB: begin
                            jump_flag_o <= `JumpDisable;
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                            sram_raddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) - ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_LH: begin
                            jump_flag_o <= `JumpDisable;
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                            sram_raddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) - ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_LW: begin
                            jump_flag_o <= `JumpDisable;
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                            sram_raddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) - ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_LBU: begin
                            jump_flag_o <= `JumpDisable;
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                            sram_raddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) - ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_LHU: begin
                            jump_flag_o <= `JumpDisable;
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]};
                            sram_raddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) - ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & 32'hfffffffc)) & 2'b11;
                        end
                    endcase
                end
                `INST_TYPE_S: begin
                    case (funct3)
                        `INST_SB: begin
                            jump_flag_o <= `JumpDisable;
                            sram_waddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
                            sram_waddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]}) - (reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]} & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_SH: begin
                            jump_flag_o <= `JumpDisable;
                            sram_waddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
                            sram_raddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
                            sram_waddr_index <= ((reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]}) - (reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]} & 32'hfffffffc)) & 2'b11;
                        end
                        `INST_SW: begin
                            jump_flag_o <= `JumpDisable;
                            sram_waddr_o <= reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
                            sram_wdata_o <= reg2_rdata_i;
                        end
                    endcase
                end
                `INST_TYPE_B: begin
                    case (funct3)
                        `INST_BEQ: begin
                            if (reg1_rdata_i == reg2_rdata_i) begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end else begin
                                jump_flag_o <= `JumpDisable;
                            end
                        end
                        `INST_BNE: begin
                            if (reg1_rdata_i != reg2_rdata_i) begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end else begin
                                jump_flag_o <= `JumpDisable;
                            end
                        end
                        `INST_BLT: begin
                            if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b0) begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                if (reg1_rdata_i >= reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b0) begin
                                if (reg1_rdata_i >= reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else begin
                                jump_flag_o <= `JumpDisable;
                            end
                        end
                        `INST_BGE: begin
                            if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b1) begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                if (reg1_rdata_i < reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b0) begin
                                if (reg1_rdata_i < reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else begin
                                jump_flag_o <= `JumpDisable;
                            end
                        end
                        `INST_BLTU: begin
                            if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b0) begin
                                jump_flag_o <= `JumpDisable;
                            end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                if (reg1_rdata_i >= reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b0) begin
                                if (reg1_rdata_i >= reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end
                        end
                        `INST_BGEU: begin
                            if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b1) begin
                                jump_flag_o <= `JumpDisable;
                            end else if (reg1_rdata_i[31] == 1'b1 && reg2_rdata_i[31] == 1'b1) begin
                                if (reg1_rdata_i < reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else if (reg1_rdata_i[31] == 1'b0 && reg2_rdata_i[31] == 1'b0) begin
                                if (reg1_rdata_i < reg2_rdata_i) begin
                                    jump_flag_o <= `JumpDisable;
                                end else begin
                                    jump_flag_o <= `JumpEnable;
                                    is_jumping <= `True;
                                    jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                                end
                            end else begin
                                jump_flag_o <= `JumpEnable;
                                is_jumping <= `True;
                                jump_addr_o <= inst_addr_i + {{20{inst_i[31]}}, inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
                            end
                        end
                    endcase
                end
                `INST_JAL: begin
					jump_flag_o <= `JumpEnable;
                    is_jumping <= `True;
                    jump_addr_o <= inst_addr_i + {{12{inst_i[31]}}, inst_i[19:12], inst_i[20], inst_i[30:21], 1'b0};
                    reg_wdata_o <= inst_addr_i + 4'h4;
                end
                `INST_JALR: begin
					jump_flag_o <= `JumpEnable;
                    is_jumping <= `True;
                    jump_addr_o <= (reg1_rdata_i + {{20{inst_i[31]}}, inst_i[31:20]}) & (32'hfffffffe);
					reg_wdata_o <= inst_addr_i + 4'h4;
				end
                `INST_LUI: begin
                    jump_flag_o <= `JumpDisable;
                    reg_wdata_o <= {inst_i[31:12], 12'b0};
                end
                `INST_AUIPC: begin
                    jump_flag_o <= `JumpDisable;
                    reg_wdata_o <= {inst_i[31:12], 12'b0} + inst_addr_i;
                end
                `INST_NOP: begin
                    jump_flag_o <= `JumpDisable;
                    is_jumping <= `False;
                end
                `INST_FENCE: begin
                    jump_flag_o <= `JumpEnable;
                    is_jumping <= `True;
                    jump_addr_o <= inst_addr_i + 4'h4;
                end
                default: begin

                end
            endcase
        end
    end

    always @ (*) begin
        if (inst_valid_i == `InstValid) begin
            case (opcode)
                `INST_TYPE_L: begin
                    case (funct3)
                        `INST_LB: begin
                            if (sram_raddr_index == 2'b0)
                                reg_wdata_o <= {{24{sram_rdata_i[7]}}, sram_rdata_i[7:0]};
                            else if (sram_raddr_index == 2'b01)
                                reg_wdata_o <= {{24{sram_rdata_i[15]}}, sram_rdata_i[15:8]};
                            else if (sram_raddr_index == 2'b10)
                                reg_wdata_o <= {{24{sram_rdata_i[23]}}, sram_rdata_i[23:16]};
                            else
                                reg_wdata_o <= {{24{sram_rdata_i[31]}}, sram_rdata_i[31:24]};
                        end
                        `INST_LH: begin
                            if (sram_raddr_index == 2'b0)
                                reg_wdata_o <= {{16{sram_rdata_i[15]}}, sram_rdata_i[15:0]};
                            else
                                reg_wdata_o <= {{16{sram_rdata_i[31]}}, sram_rdata_i[31:16]};
                        end
                        `INST_LW: begin
                            reg_wdata_o <= sram_rdata_i;
                        end
                        `INST_LBU: begin
                            if (sram_raddr_index == 2'b0)
                                reg_wdata_o <= {24'h0, sram_rdata_i[7:0]};
                            else if (sram_raddr_index == 2'b01)
                                reg_wdata_o <= {24'h0, sram_rdata_i[15:8]};
                            else if (sram_raddr_index == 2'b10)
                                reg_wdata_o <= {24'h0, sram_rdata_i[23:16]};
                            else
                                reg_wdata_o <= {24'h0, sram_rdata_i[31:24]};
                        end
                        `INST_LHU: begin
                            if (sram_raddr_index == 2'b0)
                                reg_wdata_o <= {16'h0, sram_rdata_i[15:0]};
                            else
                                reg_wdata_o <= {16'h0, sram_rdata_i[31:16]};
                        end
                    endcase
                end
                `INST_TYPE_S: begin
                    case (funct3)
                        `INST_SB: begin
                            if (sram_waddr_index == 2'b00)
                                sram_wdata_o <= {sram_rdata_i[31:8], reg2_rdata_i[7:0]};
                            else if (sram_waddr_index == 2'b01)
                                sram_wdata_o <= {sram_rdata_i[31:16], reg2_rdata_i[7:0], sram_rdata_i[7:0]};
                            else if (sram_waddr_index == 2'b10)
                                sram_wdata_o <= {sram_rdata_i[31:24], reg2_rdata_i[7:0], sram_rdata_i[15:0]};
                            else
                                sram_wdata_o <= {reg2_rdata_i[7:0], sram_rdata_i[23:0]};
                        end
                        `INST_SH: begin
                            if (sram_waddr_index == 2'b00)
                                sram_wdata_o <= {sram_rdata_i[31:16], reg2_rdata_i[15:0]};
                            else
                                sram_wdata_o <= {reg2_rdata_i[15:0], sram_rdata_i[15:0]};
                        end
                    endcase
                end
            endcase
        end
    end

endmodule
