
RType = {
    "add": "100000",
    "addu": "100001",
    "and": "100100",
    "div": "011010",
    "divu": "011011",
    "mult": "011000",
    "multu": "011001",
    "nor": "100111",
    "or": "100101",
    "sll": "000000",
    "sllv": "000100",
    "sra": "000011",
    "srav": "000111",
    "srl": "000010",
    "srlv": "000110",
    "sub": "100010",
    "subu": "100011",
    "xor": "100110",
}

IType = {
    "ori": "001101",
    "xori": "001110",
    "andi": "001100",
    "addi": "001000",
    "addiu": "001001",
    "sw": "101011",
    "lw": "100011",
    "lui": "001111",
    "beq": "000100",
    "bne": "000101",
    "bgtz": "000111",
    "blez": "000110",
}

JType = {
    "j": "000010",
    "jr": "001000",
}

registers = {
    "$zero": "00000",
    "$at": "00001",
    "$v0": "00010",
    "$v1": "00011",
    "$a0": "00100",
    "$a1": "00101",
    "$a2": "00110",
    "$a3": "00111",
    "$t0": "01000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
    "$t8": "11000",
    "$t9": "11001",
    "$k0": "11010",
    "$k1": "11011",
    "$gp": "11100",
    "$sp": "11101",
    "$fp": "11110",
    "$ra": "11111"
}

lables = {}

def getEncodingType(line):
    if line in RType:
        return "R"
    elif line in IType:
        return "I"
    elif line in JType:
        return "J"
    else:
        return None

'''
The way that the assembler combines each part of the instruction
is just about the worst way it could be done since it is using strings
to combine the raw binary values but it works so I'm not going to change it
'''
def assemble(data: bytearray):
    with open("assembly.s", "r") as file:
        for line in file:
            line = " ".join(line.split()).replace(",", "").lower()
            
            if line.endswith(":"):
                lables[line[:-1]] = len(data)
            
            op = line.split(" ")[0]
            encodingType = getEncodingType(op)

            if encodingType == "R":
                reg1 = line.split(" ")[1]
                reg2 = line.split(" ")[2]
                reg3 = line.split(" ")[3]
                shamt = "00000"
                funct = RType[line.split(" ")[0]]
                
                binary = "000000" + registers[reg2] + registers[reg3] + registers[reg1] + shamt + funct

                for i in range(0, len(binary), 8):
                    data.append(int(binary[i:i+8], 2))
            
            elif encodingType == "I":
                reg1 = line.split(" ")[1]
                reg2 = line.split(" ")[2]
                imm = ""
                if "0x" in line.split(" ")[3]:
                    imm = int(line.split(" ")[3], 16)
                else:
                    imm = int(line.split(" ")[3])

                binary = IType[op] + registers[reg2] + registers[reg1] + bin(imm)[2:].rjust(16, "0")

                for i in range(0, len(binary), 8):
                    data.append(int(binary[i:i+8], 2))

            elif encodingType == "J":
                address = ""

                if "0x" in line.split(" ")[1]:
                    address = int(line.split(" ")[1], 16)
                elif line.split(" ")[1] in lables:          
                    # divide by 4 to get the address in words
                    address = int(lables[line.split(" ")[1]] / 4)
                else:
                    address = int(line.split(" ")[1])

                binary = JType[op] + bin(address)[2:].rjust(26, "0")

                for i in range(0, len(binary), 8):
                    data.append(int(binary[i:i+8], 2))
    return data

open("output.bin", "wb").write(assemble(bytearray()))