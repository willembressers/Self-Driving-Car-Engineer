#Modify the code so that it updates the probability twice
#and gives the posterior distribution after both 
#measurements are incorporated. Make sure that your code 
#allows for any sequence of measurement of any length.

p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

def sense(p, Z):
    # loop over the probabilities
    q = [x * pHit if world[i] == Z else x * pMiss for i, x in enumerate(p)]
    
    # calculate the sum
    total = sum(q)

    # normalize 
    return list(map(lambda x: x/total, q)) 

# update the belief
for Z in measurements:
    p = sense(p, Z)

print(p)
