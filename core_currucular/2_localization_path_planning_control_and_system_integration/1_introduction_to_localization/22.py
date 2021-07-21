#Program a function that returns a new distribution 
#q, shifted to the right by U units. If U=0, q should 
#be the same as p.

p=[0, 1, 0, 0, 0]
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

def move(p, U):
    # not sure why?
    U = U % len(p)
    
    # cyclic (exact) movement
    # get the last U items (p[-U:]) and put them before all but the last U items (p[:-U])
    return p[-U:] + p[:-U]

print(move(p, 1))
