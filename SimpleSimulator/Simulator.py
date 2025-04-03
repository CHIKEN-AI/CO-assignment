import sys

register = {
    '00000': 'zero', '00001': 'ra', '00010': 'sp', '00011': 'gp',
    '00100': 'tp', '00101': 't0', '00110': 't1', '00111': 't2',
    '01000': 's0', '01001': 's1', '01010': 'a0', '01011': 'a1',
    '01100': 'a2', '01101': 'a3', '01110': 'a4', '01111': 'a5',
    '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3',
    '10100': 's4', '10101': 's5', '10110': 's6', '10111': 's7',
    '11000': 's8', '11001': 's9', '11010': 's10', '11011': 's11',
    '11100': 't3', '11101': 't4', '11110': 't5', '11111': 't6'
}
#register
values = {
    "0x"+f"{loc:08x}".upper(): 0 for loc in range(65536, 65660 + 1, 4)}
#memory values
r_val= {reg: '0'*32 for reg in register.keys()}
r_val['00010'] = '00000000000000000000000101111100'
#register values
ops={
    '0110011': {'0000000': {'000': 'add','010': 'slt','101': 'srl','110': 'or','111': 'and'},
    '0100000': {'000': 'sub'}},
    '0000011': {'': {'010': 'lw'}},
    '0010011': {'': {'000': 'addi'}},
    '1100111': {'': {'000': 'jalr'}},
    '0100011': {'': {
    '010': 'sw'}},
    '1100011': {'': {'000': 'beq','001': 'bne','100': 'blt'}},
    '1101111': {'': 'jal'}}
#Creating a dictionary of dictionary for opcode table


def copy(pc):
    str = ""
    str += format(pc, '#034b')
    for j in r_val:
        str += ' '
        str += '0b' + j
    str += '\n'
    return str


#checking instruction type

def R_type(opcode, fun7, fun3):
    if fun7 in ops[opcode] and fun3 in ops[opcode][fun7]:
        return True
    else:
        raise ValueError("UNKNOWN FUNC")
#for checking R type instructions  
def S_type(opcode, fun3):
    if '' in ops[opcode] and fun3 in ops[opcode]['']:
        return True
    else:
        raise ValueError("UNKNOWN FUNC")
#for checking S type instructions
def B_type(opcode, fun3):
    if '' in ops[opcode] and fun3 in ops[opcode]['']:
        return True
    else:
        raise ValueError("UNKNOWN FUNC")
#for checking B type instructions
def I_type(opcode, fun3):
    if '' in ops[opcode] and fun3 in ops[opcode]['']:
        return True
    else:
        raise ValueError("UNKNOWN FUNC")
#for checking I type instructions
def J_type(opcode):
    if '' in ops[opcode]:
        return True
    else:
        raise ValueError("UNKNOWN FUNC")
#for checking J type instructions

type_table = {'0110011': 'R',
              '0000011': 'I',
              '0010011': 'I',
              '1100111': 'I',
              '0100011': 'S',
              '1100011': 'B',
              '1101111': 'J'}
#type table for instruction types

def sign_comparing(a, b):
    if a[0] == '1':#for -ve
        value_a = -(2**31)+int(a[1:32], 2)
    else:#for +ve
        value_a = int(a[0:32], 2)
        #for converting a to signed integer

    if b[0] == '1':#for -ve
        value_b = -(2**31)+int(b[1:32], 2)
    else:#for +ve
        value_b = int(b[0:32], 2)
        #for converting b to signed integer

    if value_a < value_b:#compare a and b
        return True
    return False
#for comparing two signed integers

def sign_ext(x):
    if x[0] == '0':#for +ve
        x = '0'*(32-len(x))+x
    elif x[0] == '1':#for -ve
        x = '1'*(32-len(x))+x
    return x
#for sign extending to 32 bit

def bin_int(a):
    if a[0] == '0':#for +ve
        a = int(a[0:len(a)], 2)
    elif a[0] == '1':#for -ve
        a = -(2**(len(a)-1))+int(a[1:32], 2)
    return a
#binary to int



def R(opcode, fun7, rs2, rs1, fun3, rd):#executing R type instructions

    if ops[opcode][fun7][fun3] == 'add': 
        #for add 
        r_val[rd] = int(r_val[rs1], 2) + int(r_val[rs2], 2)
        r_val[rd] = bin(r_val[rd] & 0xFFFFFFFF)[2:]
        r_val[rd] = r_val[rd].zfill(32)

    elif ops[opcode][fun7][fun3] == 'slt':
        #for set less than
        if sign_comparing(r_val[rs1], r_val[rs2]) == True:
            r_val[rd] = '00000000000000000000000000000001'

    elif ops[opcode][fun7][fun3] == 'srl':
       #for srl 
        val = r_val[rs2][27:32]
        val = int(val, 2)
        r_val[rd] = r_val[rs1][0:(32-val)]
        r_val[rd] = '0'*val+r_val[rd]

    elif ops[opcode][fun7][fun3] == 'or':
        #for or
        last = []
        for i in range(32):
            if r_val[rs1][i] == '1' or r_val[rs2][i] == '1':
                last.append('1')
            elif r_val[rs1][i] == '0' and r_val[rs2][i] == '0':
                last.append('0')

        last = ''.join(last)
        r_val[rd] = last

    elif ops[opcode][fun7][fun3] == 'and':
        #for and 
        last = []
        for i in range(32):
            if r_val[rs1][i] == '1' and r_val[rs2][i] == '1':
                last.append('1')
            elif r_val[rs1][i] == '0' or r_val[rs2][i] == '0':
                last.append('0')
        last = ''.join(last)
        r_val[rd] = last

    elif ops[opcode][fun7][fun3] == 'sub':
        #for subtraction
        r_val[rd] = int(r_val[rs1], 2) - int(r_val[rs2], 2)
        r_val[rd] = bin(r_val[rd] & 0xFFFFFFFF)[2:]
        r_val[rd] = r_val[rd].zfill(32)

def S(opcode, imm, rs1, rs2, fun3, PC):#executing S type instructions
    if ops[opcode][''][fun3] == 'sw':
        imm = int(sign_ext(imm), 2) if imm[0] == '0' else int(
            sign_ext(imm), 2) - (1 << 32)
        location = int(r_val[rs1], 2) + imm
        location_hex = "0x" + format(location, '08X')
        values[location_hex] = int(r_val[rs2], 2)
        PC = PC + 4
        return PC
    


def J(opcode, imm, rd, PC):#executing J type instructions
    imm=sign_ext(imm)
    if ops[opcode][''] == 'jal':
        if imm[0]=='1':
            imm = int(imm, 2) - 1<<32
        else:
            imm=int(imm,2)
        
        r_val[rd] = format(PC + 4, '032b')
        PC = PC + imm
        return PC
    return r_val[rd]

def I(imm, rs1, fun3, rd, opcode, pc, line):#executing I type instructions
    if ops[opcode][''][fun3] == 'addi':
        imm = int(sign_ext(imm), 2) if imm[0] == '0' else int(
            sign_ext(imm), 2) - (1 << 32)
        r_val[rd] = int(r_val[rs1], 2) + imm
        r_val[rd] = format(r_val[rd] & 0xFFFFFFFF, '032b')
        return pc + 4

    if ops[opcode][''][fun3] == 'jalr':
        #for jalr
        imm = int(sign_ext(imm), 2) if imm[0] == '0' else int(
            sign_ext(imm), 2) - (1 << 32)

        new_pc = int(r_val[rs1], 2) + imm
        new_pc = new_pc & ~1
        r_val[rd] = format(pc + 4, '032b')
        return new_pc

    if ops[opcode][''][fun3] == 'lw':
        #for lw
        imm = int(sign_ext(imm), 2) if imm[0] == '0' else int(
            sign_ext(imm), 2) - (1 << 32)
        location = int(r_val[rs1], 2) + imm
        location_hex = "0x" + format(location, '08X')
        r_val[rd] = format(values[location_hex], '032b')
        return pc + 4
    


def B(opcode, imm, rs1, rs2, pc, fun3):#executing B type instructions
    imm += '0'
    imm = int(sign_ext(imm), 2) if imm[0] == '0' else int(
        sign_ext(imm), 2) - (1 << 32)

    if ops[opcode][''][fun3] == 'beq':
        #for beq
        if r_val[rs1] == r_val[rs2]:
            if imm == 0:
                return "HALT"
            return pc+imm
        return pc+4
    
    if ops[opcode][''][fun3] == 'bne':
        #for bne
        if r_val[rs1] != r_val[rs2]:
            return pc+imm
        return pc+4

    
def copy(pc):
    str = ""
    str += format(pc, '#034b')
    for j in r_val:
        str += ' '
        str += '0b' + j
    str += '\n'
    return str



def run(l,output_file):
    output = ""

    l = [x.strip() for x in l]
    l = [x for x in l if x]
    d = {}

    i = 0
    while i < len(l):
        d[i * 4] = l[i]
        i += 1
    
    pc = 0
    while pc in d:
        last_pc=pc

        line = d[pc]
        opcode = line[-7:]
        if opcode not in ops:
            raise ValueError("OPcode isn't there")
        instruction = type_table[opcode]

        if instruction == 'R':
            fun7 = line[:7]
            rs2 = line[7:12]
            rs1 = line[12:17]
            fun3 = line[17:20]
            rd = line[20:25]

            assert R_type(opcode, fun7, fun3)
            assert rs1 in register
            assert rs2 in register
            assert rd in register
            R(opcode, fun7, rs2, rs1, fun3, rd)
            pc += 4

        elif instruction == 'I':
            imm = line[:12]
            rs1 = line[12:17]
            fun3 = line[17:20]
            rd = line[20:25]
            assert I_type(opcode, fun3)
            assert rs1 in register
            pc = I(imm, rs1, fun3, rd, opcode, pc, line)

        elif instruction == 'S':
            imm = line[:7]+line[20:25]
            rs2 = line[7:12]
            rs1 = line[12:17]
            fun3 = line[17:20]
            assert S_type(opcode, fun3)
            assert rs1 in register
            assert rs2 in register
            pc = S(opcode, imm, rs1, rs2, fun3, pc)

        elif instruction == 'B':
            imm = line[0]+line[24]+line[1:7]+line[20:24]
            rs2 = line[7:12]
            rs1 = line[12:17]
            fun3 = line[17:20]
            assert B_type(opcode, fun3)
            assert rs1 in register
            assert rs2 in register
            old_pc = pc
            pc = B(opcode, imm, rs1, rs2, pc, fun3)
            if pc == "HALT":
                output += f"0b{format(old_pc, '032b')} "
                for i in r_val.keys():
                    output += f"0b{r_val[i]} "
                output += "\n"
                break #for halting the program
                        
        elif instruction == 'J':
            imm = line[0] + line[12:20] + line[11] + line[1:11]+'0'
            rd = line[20:25]
            assert rd in register
            assert J_type(opcode)
            assert rd in register
            pc = J(opcode, imm, rd, pc)
        else:
            raise ValueError("OPcode isn't there")

        if pc=='HALT':
            output += "0b" + format(int(last_pc), "032b") + " "
        else:
            output += "0b" + format(int(pc), "032b") + " "
        r_val['00000'] = "0" * 32
        for i in r_val.keys():
            output += "0b" + r_val[i] + " "
        output += "\n"

    for loc in range(65536, 65660 + 1, 4):
        output += f"0x{f"{loc:08x}".upper()}:0b{format(values["0x"+f"{loc:08x}".upper()], '032b')}\n"
    with open(output_file, "w") as f:
        f.write(output.strip())

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, "r") as f:
        l = f.readlines()
    run(l,output_file)