# Modify the empty list, p, so that it becomes a UNIFORM probability
# distribution over five grid cells, as expressed in a list of 
# five probabilities.

i = 5

p = [1./i for x in range(i)]

print(p)