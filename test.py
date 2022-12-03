class Dog:
    def __init__(self, name):
        self.name = name

sally = Dog("sally")
monty = Dog("monty")

t = {(sally, "blue"), ("hi", monty)}

if (sally, "blue") in t:
    sally.name = "happy"

print(sally.name)