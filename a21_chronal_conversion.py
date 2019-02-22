'''
NOTE: Especially for the iterations necessary for the "Day2"
part of this problem, running this code with pypy will be
MUCH faster than running it with the standard CPython.
(But it still takes awhile.)
'''

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
        self.op_count = 0   # total number of instructions performed
    
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
        
    def execute_instruction(self, echo = False):
        '''Execute the next instruction.
        Returns True on successful execution.
        Returns False on program halt.'''
        if self.pc >= len(self.prog):
            # prog counter pointing outside program
            return False
        # before op, write pc to linked register
        self.reg[self.pc_link] = self.pc
        if echo:
            print('---'*10)
            print(f'{self.op_count}  |  {self.pc}  |  {self.prog[self.pc]}')
            print(self.reg, 'Before')
        thisop = self.prog[self.pc]
        instruction = self.instructions[thisop[0]]
        func = instruction[0]
        op1 = self.resolve(instruction[1], thisop[1])  # first operand
        op2 = self.resolve(instruction[2], thisop[2])  # second operand
        self.reg[thisop[3]] = func(op1,op2)
        # After op, copy linked reg to pc and add 1
        self.pc = self.reg[self.pc_link] + 1
        self.op_count += 1
        if echo:
            print(self.reg, 'After')
        return True

if __name__ == "__main__":
    cpu = ElfCPU()
    cpu.load_program('a21_input.txt')
    # cpu.reg[0] = 6132825
    vals_seen = set()
    last_val = cpu.reg[3]
    while cpu.execute_instruction():
        # if instruction 28 evaluates to true, the program halts.
        if cpu.pc == 28:
            vals_seen.add(cpu.reg[3])
            break
    day_one_answer = cpu.reg[3]
    print(f'Day One answer: {day_one_answer}')
    # to find the value that will make the most loops,
    # we'll loop until we see our day one answer again,
    # then it's the value that came just before it.
    rounds = 1
    while cpu.execute_instruction():
        if cpu.pc == 28:
            rounds += 1
            print(rounds, cpu.reg[3])
            if cpu.reg[3] in vals_seen:
                print(f'Longest run value Day 2 Answer: {last_val}')
                print(f'Day 1 answer was: {day_one_answer}')
                break
            vals_seen.add(cpu.reg[3])
            last_val = cpu.reg[3]


