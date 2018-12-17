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

# initial state
scoreboard = [3, 7]
elves = []
elves.append(Elf(scoreboard, 0))
elves.append(Elf(scoreboard, 1))

# Find the answer
score_after_recipe = int('077201') # my puzzle input
i = 0
while i < (score_after_recipe + 10):
    scoreboard.extend(generate_recipes(elves))
    #print(scoreboard)
    for elf in elves:
        elf.step()
    i += 1

score = get_score_after_recipe(scoreboard, score_after_recipe)
print(f'Score after recipe {score_after_recipe} is: {score}')
