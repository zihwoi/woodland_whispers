class Puzzle:
    def __init__(self, name, question, answer, reward):
        self.name = name
        self.question = question
        self.answer = answer.lower()
        self.reward = reward
        self.solved = False