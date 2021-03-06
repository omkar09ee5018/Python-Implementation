# JVM PYTHON IMPLEMENTATION

import sys, string, time
import numpy as np
from constant_pool_class import Constant_Pool_Class
#import itertools


# programming stack pointer as pre-decrement for POP and post-increment for PUSH
# PC is incremented at the end of each instruction i.e. after instruction has been committed (when pipelined)
# value, result is a temp register not visible to programmers

# what to do about objects? (how to implement heap)?


def rshift(val = np.uint64, n = np.uint64):
    x = np.uint64((val % np.uint64(0x100000000)) >> n)
    return x

def readmem(address):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    # read memory needs only address lines and data is returned
    print 'read mem'
    return memory[address]

def writemem(address, value = np.uint32()):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    # write memory needs both address and data
    print 'write mem'
    #print value.dtype, value
    memory[address] = value

def POP():
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    print 'POP'
    # add sanity checks
    stack_pointer -= 1
    return readmem(stack_pointer)

def PUSH(value = np.uint32()):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    print 'PUSH'
    # add sanity checks
    #print value.dtype, value
    writemem(stack_pointer, value)
    stack_pointer += 1

def PUSH64(value = np.uint64()):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    print 'lpush'
    x = np.uint64(0xFFFFFFFF)
    y = np.uint64(32)
    print 'value', value, bin(value), value.dtype
    print 'x', x, bin(x), x.dtype
    print 'y', y, bin(y), y.dtype
    reg64_A = value & x
    print 'reg64_A', reg64_A, bin(reg64_A), reg64_A.dtype
    reg_A = reg64_A.astype('int32') # lower 32
    print 'reg_A', reg_A, bin(reg_A), reg_A.dtype
    reg64_B = value >> y
    print 'reg64_B', reg64_B, bin(reg64_B), reg64_B.dtype
    reg_B = reg64_B.astype('int32') # higher 32
    print 'reg_B', reg_B, bin(reg_B), reg_B.dtype
    PUSH(reg_B)
    PUSH(reg_A)

def ALU64_op(op):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    result64_ALU = np.int64(0)
    reg_A = POP()
    reg_B = POP()
    reg64_A = reg_B
    reg64_A = np.uint64(reg64_A << np.uint64(32))
    reg64_A = np.uint64(reg64_A | reg_A)
    reg_C = POP()
    reg_D = POP()
    reg64_B = reg_D
    reg64_B = np.uint64(reg64_B << np.uint64(32))
    reg64_B = np.uint64(reg64_B | reg_C)
    print 'reg64_B', reg64_B, bin(reg64_B), reg64_B.dtype
    print 'reg64_A', reg64_A, bin(reg64_A), reg64_A.dtype
    if op == 1:
        print 'ADD'
        result64_ALU = reg64_B + reg64_A
    elif op == 2:
        print 'SUB'
        result64_ALU = reg64_B - reg64_A
    elif op == 3:
        print 'mul'
        result64_ALU = reg64_A * reg64_B
    elif op == 4:
        print 'div'
        result64_ALU = reg64_B / reg64_A
    elif op == 5:
        print 'rem'
        result64_ALU = reg64_B - (reg64_B/reg64_A) * reg64_A
    elif op == 6:       # left shift
        print 'l l shift'
        reg64_B = reg64_B & np.uint64(63)
        result64_ALU = reg64_A << reg64_B
    elif op == 7:
        print 'lAND'
        result64_ALU = reg64_A & reg64_B
    elif op == 8:
        print 'lOR'
        result64_ALU = reg64_A | reg64_B
    elif op == 9:
        print 'lXOR'
        result64_ALU = reg64_A ^ reg64_B
    print 'result64_ALU', result64_ALU, bin(result64_ALU), result64_ALU.dtype, result64_ALU.astype(np.int64)
    #return result64_ALU.astype(np.int64)
    return result64_ALU

def ALU_op(op):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    print 'ALU OPERATION',
    # pop TOS & TOS-1
    reg_B = POP()   #value2
    reg_A = POP()   #value1
    result_ALU = np.uint32(0)
    print 'reg_B', bin(reg_B), reg_B.dtype
    print 'reg_A', bin(reg_A), reg_A.dtype
    if op == 1:
        print 'ADD'
        result_ALU = reg_A + reg_B
    elif op == 2:
        print 'SUB'
        result_ALU = reg_A - reg_B
    elif op == 3:
        print 'AND'
        result_ALU = reg_A & reg_B
    elif op == 4:
        print 'OR'
        result_ALU = reg_A | reg_B
    elif op == 5:       # left shift
        print 'l i shift'
        reg_B = reg_B & np.uint32(31)
        result_ALU = reg_A << reg_B
    elif op == 6:
        print 'rem'
        result_ALU = reg_B - (reg_B/reg_A) * reg_A
    elif op == 7:
        print 'imul'
        print 'check what happens due to overflow'
        result_ALU = reg_A * reg_B
    elif op == 8:
        print 'idiv'
        print 'check what happens due to underflow'
        result_ALU = reg_A / reg_B
    elif op == 9:
        print 'ixor'
        result_ALU = reg_A ^ reg_B

    # push result onto stack
    #stack[stack_pointer] = result_ALU
    writemem(stack_pointer, result_ALU)
    stack_pointer += 1

def IF(type):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size

    reg_A = np.uint32(POP())
    result = np.uint32(0)

    if type == 1:
        result = (reg_A == np.uint32(0))   # ifeq
    elif type == 2:
        result = (reg_A != np.uint32(0))   # ifne
    elif type == 3:
        result = (reg_A < np.uint32(0))   # iflt
    elif type == 4:
        result = (reg_A <= np.uint32(0))   # ifle
    elif type == 5:
        result = (reg_A > np.uint32(0))   # ifgt
    elif type == 6:
        result = (reg_A >= np.uint32(0))   # ifge

    if result:          #if true
        offset = OFFSET()
        JUMP(offset)
    else:
        PC += 2


def compare(type):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size

    #pop TOS & TOS-1

    reg_B = POP()
    reg_A = POP()
    result = np.uint32(0)

    #compare
    if type == 1:
        result = (reg_A == reg_B)   # eq
    elif type == 2:
        result = (reg_A != reg_B)   # ne
    elif type == 3:
        result = (reg_A < reg_B)   # lt
    elif type == 6:
        result = (reg_A <= reg_B)   # le
    elif type == 4:
        result = (reg_A >= reg_B)   # ge
    elif type == 5:
        result = (reg_A > reg_B)   # gt

    if result:          #if true
        offset = OFFSET()
        JUMP(offset)
    else:
        PC += 2

def INC():
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    # reprogram using alu_operation(add)
    # push local variable onto the stack
    # add 1 to stack might need extra space on the stack to implement
    print 'inc'
    PC += 1
    reg = readmem(PC)     # index      reg is temp register
    PC += 1
    reg_A = readmem(PC)     #const
    reg_B = readmem(local_var_ptr+reg)

    if reg_A & np.uint32(0b10000000):
        reg_A = np.uint32(256) - reg_A
        reg_B = reg_B - reg_A
    else:
        reg_B = reg_A + reg_B
    writemem(local_var_ptr+reg, reg_B)

def OFFSET():
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    # reg_A = int(method_area[PC+1], 16)
    reg_A = readmem(PC+1)
    # reg_B = int(method_area[PC+2], 16)
    reg_B = readmem(PC+2)
    # limit int to two bytes
    reg_A = reg_A << 8
    offset = reg_A | reg_B
    return offset

def JUMP(offset):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size

    if offset & np.uint32(0x8000):
        offset = np.uint32(65536) - offset
        PC = PC - offset
    else:
        PC = PC + offset
    PC = PC- 1

def signExtension32to64(value = np.uint32()):
    temp = (np.uint64(0x00000000FFFFFFFF) & value)
    mask = np.uint32(0x80000000)
    sign = np.uint32((mask & value) >> np.uint32(32))
    if (mask & value):
        temp += np.uint64(0xFFFFFFFF00000000)
    return temp

def signExtension16to32(instr = np.uint32()):
    value = (np.uint32(0x0000FFFF) & instr)
    mask = np.uint32(0x00008000)
    sign = np.uint32((mask & instr) >> 15)
    if sign == 1:
        value += 0xFFFF0000
    return value

#def signExtension16to32(instr = np.uint32()):
#    value = (0x000000FF & instr)
#    mask = 0x00000080
#    sign = (mask & instr) >> 15
#    if sign == 1:
#        value += 0xFFFFFF00
#    return value



def get_method_info(filename):
    global stack, stack_size, local_var, stack_pointer, method_area, reg_A, reg_B, memory, local_var_ptr, reg64_A, reg64_B, reg_C, reg_D, PC, local_size
    file = open(filename, 'r')
    lines = file.readlines()
    for x in range(len(lines)):
        line = lines[x].rstrip('\n')
        inst = string.split(line)
        print inst
        if line == "code":
            _method_area = lines[x+1]
            method_area = [i+j for i, j in zip(_method_area[::2], _method_area[1::2])]
            print method_area
            print 'len of bytecode:', len(method_area)
        elif inst[0] == 'stack':
            stack_size = int(inst[2], 16)
        elif inst[0] == 'locals':
            local_size = int(inst[2], 16)

def dump():
    file1.write('\n')
    print 'MEMORY:', memory[local_var_ptr:]
    file1.write(' PC: ')
    file1.write(str(PC))
    file1.write(' local var: ')
    file1.write(str(memory[local_var_ptr:local_var_ptr+local_size]))
    file1.write('\n')
    file1.write('Stack: ')
    file1.write(str(memory[stack_base:]))
    file1.write(' Stack Depth: ')
    file1.write(str(stack_pointer-stack_base))
    file1.write('\n')
    file1.write('Heap: ')
    file1.write(str(heap_ptr))
    file1.write('\n')

if __name__ == "__main__":
    filename = sys.argv[1]
    line_num = 1
    method_area = []
    stack_size = 0
    get_method_info(filename)
    stack = [0] * stack_size
    local_var = [0] * local_size
    PC = 0
    reg_A = np.uint32(0)
    reg_B = np.uint32(0)
    reg_C = np.uint32(0)
    reg_D = np.uint32(0)
    reg64_A = np.uint64(0)
    reg64_B = np.uint64(0)
    reg64_C = np.uint64(0)
    stack_pointer = 0
    heap = [0]*100
    heap_base = 0
    heap_ptr = 0
    shift = 0
    for x in range(0, len(method_area)):
        method_area[x] = int(method_area[x], 16)
    #print method_area
    stack_base = len(method_area) + local_size
    stack_pointer = len(method_area) + local_size
    local_var_ptr = len(method_area)
    C_pool = Constant_Pool_Class()
    constant_pool = C_pool.ReadConstantPool()
    print 'Constant Pool:', constant_pool
    memory = np.array(method_area + local_var + stack, dtype='uint32')
    filename1 = 'debug.txt'
    file1 = open(filename1, 'w')
    dump()

    while PC <= len(method_area):
        # instruction fetch

        print '------------'
        print 'PC:', PC
        print 'SP:', stack_pointer
        inst_reg = readmem(PC)
        # decode & execute

        print line_num, '::', inst_reg, ':',
        #print inst_list[inst_reg][0],
        if inst_reg == 0:
            print 'NOP'
        elif inst_reg == 1:
            file1.write('aconst_null')
            print 'aconst_null'
            PUSH(np.uint32(0b000000000))
        elif inst_reg == 2:
            file1.write('iconst_-1')
            print 'iconst-1'
            PUSH(np.int32(-1))
        elif inst_reg == 3:
            file1.write('iconst_0')
            print 'iconst0'
            PUSH(np.uint32(0))
        elif inst_reg == 4:
            file1.write('iconst_1')
            print 'iconst1'
            PUSH(np.uint32(1))
        elif inst_reg == 5:
            file1.write('iconst_2')
            print 'iconst2'
            PUSH(np.uint32(2))
        elif inst_reg == 6:
            file1.write('iconst_3')
            print 'iconst3'
            PUSH(np.uint32(3))
        elif inst_reg == 7:
            file1.write('iconst_4')
            print 'iconst4'
            PUSH(np.uint32(4))
        elif inst_reg == 8:
            file1.write('iconst_5')
            print 'iconst5'
            PUSH(np.uint32(5))
        elif inst_reg == 9:
            file1.write('lconst_0')
            print 'lconst0'
            PUSH(np.uint32(0))
            PUSH(np.uint32(0))
        elif inst_reg == 10:
            file1.write('lconst_1')
            print 'lconst1'
            # big-endian config
            PUSH(np.uint32(0))
            PUSH(np.uint32(1))
        elif inst_reg == 16:
            file1.write('bipush')
            print 'bipush'
            PC += 1
            PUSH(readmem(PC))
        elif inst_reg == 17:
            file1.write('sipush')
            print 'sipush'
            reg_A = OFFSET()
            PC += 2
            PUSH(reg_A)
        elif inst_reg == 18:
            file1.write('ldc')
            print 'ldc'
            reg_A = readmem(PC+1)
            PC += 1
            print 'Constant pool entry:', constant_pool[reg_A-1][1]
            reg_B = int(constant_pool[reg_A-1][1], 16)
            PUSH(reg_B)
        elif inst_reg == 19:
            file1.write('ldc_w')
            print 'ldc_w'
            offset = OFFSET()
            PC += 2
            print 'Constant Pool Entry:', constant_pool[offset-1][1]
            reg_B = int(constant_pool[offset-1][1], 16)
            PUSH(reg_B)
        elif inst_reg == 20:
            file1.write('ldc2_w')
            print 'ldc2_w'
            offset = OFFSET()
            PC += 2
            print 'Constant Pool Entry:', constant_pool[offset-1][1]
            print 'Constant Pool Entry:', constant_pool[offset][1]
            reg_B = np.uint32(int(constant_pool[offset-1][1], 16))
            reg_A = np.uint32(int(constant_pool[offset][1], 16))
            PUSH(reg_B)
            PUSH(reg_A)
        elif inst_reg == 21:
            file1.write('iload + 1 operand')
            print 'iload + 1 operand'
            reg = int(method_area[PC+1])
            PUSH(memory[local_var_ptr+reg])
            PC += 1
        elif inst_reg == 22:
            file1.write('lload + 1 operand')
            print 'lload + 1 operand'
            reg = readmem(PC+1)
            PC += 1
            reg_A = readmem(local_var_ptr+reg)
            PUSH(reg_A)
            reg_A = readmem(local_var_ptr+reg+1)
            PUSH(reg_A)
        elif inst_reg == 25:
            file1.write('aload + 1 operand')
            print 'aload + 1 operand'
            reg = readmem(PC+1)
            PC += 1
            reg_A = readmem(local_var_ptr+reg)
            PUSH(reg_A)
        elif inst_reg == 26:
            file1.write('iload_0')
            print 'iload0'
            PUSH(memory[local_var_ptr])
        elif inst_reg == 27:
            file1.write('iload_1')
            print 'iload1'
            PUSH(memory[local_var_ptr+1])
        elif inst_reg == 28:
            file1.write('iload_2')
            print 'iload2'
            PUSH(memory[local_var_ptr+2])
        elif inst_reg == 29:
            file1.write('iload_3')
            print 'iload3'
            PUSH(memory[local_var_ptr+3])
        elif inst_reg == 30:
            file1.write('lload_0')
            print 'lload_0'
            reg_A = readmem(local_var_ptr)
            reg_A = readmem(local_var_ptr)
            reg_B = readmem(local_var_ptr+1)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 31:
            file1.write('lload_1')
            print 'lload_1'
            reg_A = readmem(local_var_ptr+1)
            reg_B = readmem(local_var_ptr+2)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 32:
            file1.write('lload_2')
            print 'lload_2'
            reg_A = readmem(local_var_ptr+2)
            reg_B = readmem(local_var_ptr+3)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 33:
            file1.write('lload_3')
            print 'lload_3'
            reg_A = readmem(local_var_ptr+3)
            reg_B = readmem(local_var_ptr+4)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 42:
            file1.write('aload_0')
            print 'aload_0'
            reg_A = readmem(local_var_ptr)
            PUSH(reg_A)
        elif inst_reg == 43:
            file1.write('aload_1')
            print 'aload_1'
            reg_A = readmem(local_var_ptr+1)
            PUSH(reg_A)
        elif inst_reg == 44:
            file1.write('aload_2')
            print 'aload_2'
            reg_A = readmem(local_var_ptr+2)
            PUSH(reg_A)
        elif inst_reg == 45:
            file1.write('aload_3')
            print 'aload_3'
            reg_A = readmem(local_var_ptr+3)
            PUSH(reg_A)
        elif inst_reg == 54:
            file1.write('istore + 1 operand')
            print 'istore + 1 operand'
            reg = int(method_area[PC+1])
            value = POP()
            writemem(local_var_ptr+reg, value)
            PC += 1
        elif inst_reg == 55:
            file1.write('lstore + 1 operand')
            print 'lstore + 1 operand'
            reg = int(method_area[PC+1])
            reg_A = POP()
            reg_B = POP()
            writemem(local_var_ptr+reg, reg_B)
            writemem(local_var_ptr+reg+1, reg_A)
            PC += 1
        elif inst_reg == 59:
            file1.write('istore_0')
            print 'istore0'
            value = POP()
            writemem(local_var_ptr, value)
        elif inst_reg == 60:
            file1.write('istore_1')
            print 'istore1'
            value = POP()
            writemem(local_var_ptr+1, value)
        elif inst_reg == 61:
            file1.write('istore_2')
            print 'istore2'
            value = POP()
            writemem(local_var_ptr+2, value)
        elif inst_reg == 62:
            file1.write('istore_3')
            print 'istore3'
            value = POP()
            writemem(local_var_ptr+3, value)
        elif inst_reg == 63:
            file1.write('lstore_0')
            print 'lstore_0'
            reg_A = POP()
            reg_B = POP()
            writemem(local_var_ptr+0, reg_B)
            writemem(local_var_ptr+1, reg_A)
        elif inst_reg == 64:
            file1.write('lstore_1')
            print 'lstore_1'
            reg_A = POP()
            reg_B = POP()
            writemem(local_var_ptr+1, reg_B)
            writemem(local_var_ptr+2, reg_A)
        elif inst_reg == 65:
            file1.write('lstore_2')
            print 'lstore_2'
            reg_A = POP()
            reg_B = POP()
            writemem(local_var_ptr+2, reg_B)
            writemem(local_var_ptr+3, reg_A)
        elif inst_reg == 66:
            file1.write('lstore_3')
            print 'lstore_3'
            reg_A = POP()
            reg_B = POP()
            writemem(local_var_ptr+3, reg_B)
            writemem(local_var_ptr+4, reg_A)
        elif inst_reg == 75:
            file1.write('astore_0')
            print 'astore_0'
            reg_A = POP()
            writemem(local_var_ptr, reg_A)
        elif inst_reg == 76:
            file1.write('astore_1')
            print 'astore_1'
            reg_A = POP()
            writemem(local_var_ptr+1, reg_A)
        elif inst_reg == 77:
            file1.write('astore_2')
            print 'astore_2'
            reg_A = POP()
            writemem(local_var_ptr+2, reg_A)
        elif inst_reg == 78:
            file1.write('astore_3')
            print 'astore_3'
            reg_A = POP()
            writemem(local_var_ptr+3, reg_A)
        elif inst_reg == 79:
            file1.write('iastore')
            print 'iastore'
            reg_A = POP()       # value
            reg_B = POP()       # index
            reg_C = POP()       # arrayref
            heap[reg_C+reg_B] = reg_A
            print 'heap', heap

        elif inst_reg == 87:
            file1.write('pop')
            file1.write('#careful with this one')
            print 'pop'
            reg_A = POP()
        elif inst_reg == 88:
            file1.write('pop_2')
            print 'pop 2'
            reg_A = POP()
            reg_B = POP()
        elif inst_reg == 89:
            file1.write('dup')
            print 'dup'
            reg_A = POP()
            PUSH(reg_A)
            PUSH(reg_A)
        elif inst_reg == 90:
            file1.write('dup_x1')
            print 'dup_x1'
            reg_A = POP()       # tos
            reg_B = POP()       # tos-1
            PUSH(reg_A)
            PUSH(reg_B)
            PUSH(reg_A)
        elif inst_reg == 91:
            file1.write('dup_x2')
            print 'dup_x2'
            reg_A = POP()       # tos
            reg_B = POP()       # tos-1
            reg_C = POP()
            PUSH(reg_A)
            PUSH(reg_B)
            PUSH(reg_C)
            PUSH(reg_A)
        elif inst_reg == 92:
            file1.write('dup2')
            print 'dup2'
            reg_A = POP()       # tos
            reg_B = POP()       # tos-1
            PUSH(reg_A)
            PUSH(reg_B)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 93:
            file1.write('dup2_x1')
            print 'dup2_x1'
            print 'two types possible, need to handle'
            reg_A = POP()       # tos
            reg_B = POP()       # tos-1
            reg_C = POP()
            PUSH(reg_A)
            PUSH(reg_B)
            PUSH(reg_C)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 94:
            file1.write('dup2_x2')
            print 'dup2_x2'
            print 'two types possible, need to handle'
            reg_A = POP()       # tos
            reg_B = POP()       # tos-1
            reg_C = POP()
            reg_D = POP()
            PUSH(reg_A)
            PUSH(reg_B)
            PUSH(reg_C)
            PUSH(reg_D)
            PUSH(reg_A)
            PUSH(reg_B)
        elif inst_reg == 95:
            file1.write('swap')
            print 'swap'
            reg_A = POP()
            reg_B = POP()
            PUSH(reg_B)
            PUSH(reg_A)
        elif inst_reg == 96:
            file1.write('iadd')
            print 'iadd'
            ALU_op(1)
        elif inst_reg == 97:
            file1.write('ladd')
            print 'ladd'
            reg64_C = ALU64_op(1)
            PUSH64(reg64_C)
        elif inst_reg == 100:
            file1.write('isub')
            print 'isub'
            ALU_op(2)
        elif inst_reg == 101:
            file1.write('lsub')
            print 'lsub'
            reg64_C = ALU64_op(2)
            PUSH64(reg64_C)
        elif inst_reg == 104:
            file1.write('imul')
            print 'imul'
            ALU_op(7)
        elif inst_reg == 105:
            file1.write('lmul')
            print 'lmul'
            reg64_C = ALU64_op(3)
            PUSH64(reg64_C)
        elif inst_reg == 108:
            file1.write('idiv')
            print 'idiv'
            ALU_op(8)
        elif inst_reg == 109:
            file1.write('ldiv')
            print 'ldiv'
            reg64_C = ALU64_op(4)
            PUSH64(reg64_C)
        elif inst_reg == 112:
            file1.write('irem')
            print 'irem'
            ALU_op(6)
        elif inst_reg == 113:
            file1.write('lrem')
            print 'lrem'
            reg64_C = ALU64_op(5)
            PUSH64(reg64_C)
        elif inst_reg == 116:
            # handle redo bullshit WTF shameful
            file1.write('ineg')
            print 'ineg'
            reg_A = POP()
            reg_B = 0 - reg_A
            PUSH(reg_B)
        elif inst_reg == 117:
            # handle redo bullshit WTF shameful
            file1.write('lneg')
            print 'lneg'
        elif inst_reg == 120:
            file1.write('ishl')
            print('ishl')
            ALU_op(5)
        elif inst_reg == 121:
            file1.write('lshl')
            print('lshl')
            reg64_C = ALU64_op(6)
            PUSH64(reg64_C)
        elif inst_reg == 122:
            file1.write('ishr')
            print('ishr')
            reg_A = POP()       #value2
            reg_B = POP()       #value1
            reg_A = reg_A & 31
            reg_C = rshift(reg_B, reg_A)
            PUSH(reg_C)
        elif inst_reg == 123:
            file1.write('lshr')
            print('lshr')
            reg_A = POP()
            reg_B = POP()
            reg64_A = reg_A
            reg64_A = reg64_A << 32       #value2
            reg_C = POP()       #value1
            reg_A = reg_A & 31
            reg64_B = rshift(reg64_A, reg_C)
            PUSH64(reg64_B)
        elif inst_reg == 124:
            file1.write('iushr')
            print('iushr')
            reg_A = POP()       #value2
            reg_B = POP()       #value1
            reg_A = reg_A & 31
            reg_C = reg_B >> reg_A
            PUSH(reg_C)
        elif inst_reg == 125:
            file1.write('lushr')
            print('lushr')
            reg_A = POP()
            reg_B = POP()
            reg64_A = reg_A
            reg64_A = reg64_A << 32       #value2
            reg_C = POP()       #value1
            reg_A = reg_A & 63
            reg64_B = reg64_A >> reg_A
            PUSH64(reg64_B)
        elif inst_reg == 126:
            file1.write('iAND')
            print 'iAND'
            ALU_op(3)
        elif inst_reg == 127:
            file1.write('lAND')
            print 'lAND'
            reg64_C = ALU64_op(7)
            PUSH64(reg64_C)
        elif inst_reg == 128:
            file1.write('ior')
            print 'ior'
            ALU_op(4)
        elif inst_reg == 129:
            file1.write('lOR')
            print 'lOR'
            reg64_C = ALU64_op(8)
            PUSH64(reg64_C)
        elif inst_reg == 130:
            file1.write('iXOR')
            print 'ixor'
            ALU_op(4)
        elif inst_reg == 131:
            file1.write('lXOR')
            print 'lxor'
            reg64_C = ALU64_op(9)
            PUSH64(reg64_C)
        elif inst_reg == 132:
            file1.write('iinc + 2 operands')
            print 'iinc + 2 operands'
            INC()
        elif inst_reg == 133:
            file1.write('i2l')
            print 'i2l'
            reg_A = POP()
            reg64_A = signExtension32to64(reg_A)
            PUSH64(reg64_A)
        elif inst_reg == 136:
            file1.write('l2i')
            print 'l2i'
            reg_A = POP()
            reg_B = POP()
            PUSH(reg_B)
        elif inst_reg == 145:
            file1.write('i2b')
            print 'i2b'
            reg_A = POP()
            reg_B = reg_A & 0x000000FF
            reg_C = signExtension16to32(reg_B)
        elif inst_reg == 153:
            file1.write('ifeq')
            print 'ifeq'
            IF(1)
        elif inst_reg == 154:
            file1.write('ifne')
            print 'ifne'
            IF(2)
        elif inst_reg == 155:
            file1.write('iflt')
            print 'iflt'
            IF(4)
        elif inst_reg == 156:
            file1.write('ifge')
            print 'ifge'
            IF(5)
        elif inst_reg == 158:
            file1.write('ifle')
            print 'ifle'
            IF(6)
        elif inst_reg == 159:
            file1.write('if_icmpeq + 2 operands (equal to)')
            print 'if_icmpeq + 2 operands (equal to)'
            compare(1)
        elif inst_reg == 160:
            file1.write('if_icmpne + 2 operands (not equal to)')
            print 'if_icmpne + 2 operands (not equal to)'
            compare(2)
        elif inst_reg == 161:
            file1.write('if_icmplt + 2 operands (less then)')
            print 'if_icmplt + 2 operands (less then)'
            compare(3)
        elif inst_reg == 162:
            file1.write('if_icmpge + 2 operands (greater than or equal to)')
            print 'if_icmpge + 2 operands (greater than or equal to)'
            compare(4)
        elif inst_reg == 163:
            file1.write('if_icmpgt + 2 operands (greater than)')
            print 'if_icmpgt + 2 operands (greater than)'
            compare(5)
        elif inst_reg == 164:
            file1.write('if_icmple + 2 operands (less then or equal to)')
            print 'if_icmple + 2 operands (less then or equal to)'
            compare(6)
        elif inst_reg == 167:
            file1.write('goto + 2 operands')
            print 'goto + 2 operands'
            offset = OFFSET()
            JUMP(offset)
            print "-----------------------------------------------------------------"
        elif inst_reg == 169:
            file1.write('ret + 1 operand')
            print 'ret + 1 operand'
            PC += 1
            reg_A = readmem(PC)
            PC = reg_A-1
            break
        elif inst_reg == 177:
            file1.write('return')
            print 'return'
            print 'local_var:',
            print memory[local_var_ptr:local_var_ptr+local_size]
            exit()
        elif inst_reg == 188:
            # dont know what Im doing yet
            file1.write('newarray')
            print 'newarray'
            reg_A = POP()   # count i.e. number of elements
            PUSH(heap_ptr)      # push array ref onto the stack
            reg_B = readmem(PC+1)       # get type of array
            PC += 1
            if reg_B == 10:
                heap_ptr += reg_A
            elif reg_B == 11:
                heap_ptr += (reg_A*2)

        else:
            print '!@#$%^&*)_!@#$%^&*()_!@#$%^&*()_'
            file1.write('!@#$%^&*)_!@#$%^&*()_!@#$%^&*()_')
            exit()
        #no_of_operands = int(inst_list[memory[PC]][1])
        #if no_of_operands > 0:
            #for m in range(1, no_of_operands+1):
                #PC += 1
                #print '->', 'operand', m, ':', memory[PC],
        line_num += 1

        PC += 1
        dump()
