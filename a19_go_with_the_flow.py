# instructions:
   # opcode | input A | input B | output C
   # output is always a register number
   # 16 opcodes - interpret A and B
     # "value A" - number given as A is interpreted as an immediate literal value
     # "register A" - use the value in the register with that number

class ElfCPU(object):

    instructions = {
        'addr': [lambda a,b:a+b, 'r','r'],
        'addi': [lambda a,b:a+b, 'r','i'],
        'mulr': [lambda a,b:a*b, 'r','r'],
        'muli': [lambda a,b:a*b, 'r','i'],
        'banr': [lambda a,b:a&b, 'r','r'],
        'bani': [lambda a,b:a&b, 'r','i'],
        'borr': [lambda a,b:a|b, 'r','r'],
        'bori': [lambda a,b:a|b, 'r','i'],
        'setr': [lambda a,b:a,   'r','i'],
        'seti': [lambda a,b:a,   'i','i'],
        'gtir': [lambda a,b:int(a>b), 'i','r'],
        'gtri': [lambda a,b:int(a>b), 'r','i'],
        'gtrr': [lambda a,b:int(a>b), 'r','r'],
        'eqir': [lambda a,b:int(a==b), 'i','r'],
        'eqri': [lambda a,b:int(a==b), 'r','i'],
        'eqrr': [lambda a,b:int(a==b), 'r','r']
    }

    def __init__(self):
        self.pc = 0
        self.reg = [0 for _ in range(6)]
        self.pc_link = 0
        self.prog = list()
    
    def load_program(self, prog_file):
        self.prog = list()
        with open(prog_file, 'r') as f:
            for line in f:
                cmd = line.split()
                if cmd[0] == '#ip':
                    self.pc_link = int(cmd[1])
                else:
                    self.prog.append(
                        (cmd[0], int(cmd[1]), int(cmd[2]), int(cmd[3]))
                    )
    
    def resolve(self, selector, value):
        '''selector = 'r' or 'i'
        value is the value from instruction
        registers is the set of current register values'''
        if selector == 'i':
            return value
        if selector == 'r':
            return self.reg[value]
        raise RuntimeError(f'Invalid selector: {selector}')
        
    def execute_instruction(self):
        '''Execute the next instruction.
        Returns True on successful execution.
        Returns False on program halt.'''
        if self.pc >= len(self.prog):
            # prog counter pointing outside program
            return False
        # before op, write pc to linked register
        self.reg[self.pc_link] = self.pc
        thisop = self.prog[self.pc]
        instruction = self.instructions[thisop[0]]
        func = instruction[0]
        op1 = self.resolve(instruction[1], thisop[1])  # first operand
        op2 = self.resolve(instruction[2], thisop[2])  # second operand
        self.reg[thisop[3]] = func(op1,op2)
        # After op, copy linked reg to pc and add 1
        self.pc = self.reg[self.pc_link] + 1
        return True

if __name__=="__main__":
    cpu = ElfCPU()
    cpu.load_program('a19_input.txt')
    print(f'cpu.pc_link = {cpu.pc_link}')
    print('Program loaded:')
    for instruction in cpu.prog:
        print(instruction)
    while cpu.execute_instruction():
        # print(cpu.pc, cpu.reg)
        pass
    print(f'Value in reg 0 after halt: {cpu.reg[0]}')
