from collections import deque

class Elf(object):

    def __init__(self, scoreboard, current_recipe):
        self.scoreboard = scoreboard
        self.current_recipe = current_recipe

    def current_recipe_score(self):
        return self.scoreboard[self.current_recipe]

    def step(self):
        '''Move Elf to next recipe'''
        next_recipe = ((1 + self.current_recipe_score()) + self.current_recipe) % len(self.scoreboard)
        #print(f'Elf moves from {self.current_recipe} to {next_recipe}')
        self.current_recipe = next_recipe
    
def generate_recipes(elves):
    sum_of_current_scores = 0
    for elf in elves:
        sum_of_current_scores += elf.current_recipe_score()
    #print(f'Sum of scores: {sum_of_current_scores}')
    additional_recipes = [int(digit) for digit in str(sum_of_current_scores)]
    #print(f'Additional recipes: {additional_recipes}')
    return additional_recipes

def get_score_after_recipe(scoreboard, recipe):
    return ''.join([str(x) for x in scoreboard[recipe:recipe+10]])

def run_simulation(end_condition):
    # initial state
    scoreboard = [3, 7]
    elves = []
    elves.append(Elf(scoreboard, 0))
    elves.append(Elf(scoreboard, 1))

    # Find the answer
    current_check = deque([' '] * len(end_condition))
    match_found = False

    while True:
        # print(scoreboard)
        new_recipies = generate_recipes(elves)
        for recipie in new_recipies:
            current_check.append(str(recipie))
            current_check.popleft()
            scoreboard.append(recipie)
            check = ''.join(current_check)
            # print(check, end_condition)
            if check == end_condition:
                # print('MATCH')
                match_found = True
                break
        if match_found:
            break
        for elf in elves:
            elf.step()
    answer = len(scoreboard) - len(end_condition)    
    return answer

'''
assert run_simulation('51589') == 9
assert run_simulation('01245') == 5
assert run_simulation('92510') == 18
assert run_simulation('59414') == 2018
'''

# Be aware, this took about 7 minutes to run on my machine.
print('My answer: ' + str(run_simulation('077201')))
