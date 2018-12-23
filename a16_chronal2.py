
# instructions:
   # opcode | input A | input B | output C
   # output is always a register number
   # 16 opcodes - interpret A and B
     # "value A" - number given as A is interpreted as an immediate literal value
     # "register A" - use the value in the register with that number

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

def read_examples(filename):
    '''Read in the instruction examples.'''
    examples = []
    with open(filename, 'r') as f:
        example = {}
        for line in f:
            line = line.strip()
            if line.strip():
                if 'Before' in line:
                    line = line[line.index('[')+1:line.index(']')]
                    # new dict
                    example = {'before': [int(x) for x in line.split(',')]}
                elif 'After' in line:
                    line = line[line.index('[')+1:line.index(']')]
                    example['after'] = [int(x) for x in line.split(',')]
                    examples.append(example)
                else:
                    example['instruction'] = [int(x) for x in line.split()]
    return examples

def resolve(selector, value, registers):
    '''selector = 'r' or 'i'
    value is the value from instruction
    registers is the set of current register values'''
    if selector == 'i':
        return value
    if selector == 'r':
        return registers[value]
    raise RuntimeError(f'Invalid selector: {selector}')

def eval(instruction, registers, a, b, c):
    '''Given an instruction definition from the instruction dictionary,
    the current values of the registers, and the values of
    a, b, and c provided in the instruction, return the post-instruction
    values of the registers.'''
    reg = registers[:]   # take a copy, don't want to alter originals
    func = instruction[0]
    op1 = resolve(instruction[1], a, reg)  # first operand
    op2 = resolve(instruction[2], b, reg)  # second operand
    reg[c] = func(op1,op2)
    return reg           # return updated copy of registers

def possible_instructions(example):
    '''Return a set of possible instructions for a given example state'''
    possibilities = set()
    for opcode, instruction in instructions.items():
        test_output = eval(instruction, example['before'], *example['instruction'][1:])
        if example['after'] == test_output:
            possibilities.add(opcode)
    return possibilities

def part1():
    behave_like_3_or_more_opcodes = 0
    examples = read_examples('a16_input1.txt')
    for example in examples:
        if len(possible_instructions(example)) >= 3:
            behave_like_3_or_more_opcodes += 1
    print(f'Part 1: samples that behave like 3 or more opcodes: {behave_like_3_or_more_opcodes}')

part1()

def best_guess(examples):
    '''Given the set of examples, take the best first guess we can
    on which instructions may map to opcodes (0-15).'''
    guesses = [set() for _ in range(0,16)]
    for example in examples:
        opcode_id = example['instruction'][0]
        possibile = possible_instructions(example)
        if not guesses[opcode_id]:
            guesses[opcode_id].update(possibile)
        else:
            guesses[opcode_id].intersection_update(possibile)
    return guesses


def run_program(opcode_map, program):
    '''Using the provided opcode_map, execute the instructions of the program.'''
    registers = [0, 0, 0, 0]
    for instruction in program:
        registers = eval(instructions[opcode_map[instruction[0]]], registers, *instruction[1:])
    return registers

def refine_guesses(guess_sets):
    '''Our first guess has lots of opcodes that may represent more than one
    instruction.  But it has some that represent a single instruction, so those
    instructions are not valid possiblities for other opcodes and can be removed.
    Keep removing known instructions from opcodes with multiple possiblities until
    every opcode has only a single remaining possibility.'''
    while [g for g in guess_sets if len(g) > 1]:
        for x in [g for g in guess_sets if len(g) == 1]:
            for j,_ in [g for g in enumerate(guess_sets) if len(g[1]) > 1]:
                guess_sets[j].difference_update(x)
    return guess_sets

def part2():
    examples = read_examples('a16_input1.txt')
    guess_sets = best_guess(examples)
    guess_sets = refine_guesses(guess_sets)
    opcode_map = [list(g)[0] for g in guess_sets]
    program = []
    with open('a16_input2.txt', 'r') as f:
        for line in f:
            program.append([int(x) for x in line.strip().split()])
    result = run_program(opcode_map, program)
    print(f'Final register values: {result}')
    print(f'Part 2: register 0 value: {result[0]}')

part2()


