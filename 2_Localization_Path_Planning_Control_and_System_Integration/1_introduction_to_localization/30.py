#Given the list motions=[1,1] which means the robot 
#moves right and then right again, compute the posterior 
#distribution if the robot first senses red, then moves 
#right one, then senses green, then moves right again, 
#starting with a uniform prior distribution.

p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    # loop over the probabilities
    q = [x * pHit if world[i] == Z else x * pMiss for i, x in enumerate(p)]
    
    # calculate the sum
    total = sum(q)

    # normalize 
    return list(map(lambda x: x/total, q)) 

def move(p, U):
    q = []
    for i in range(len(p)):
        # calculate probability (when exact)
        exact = p[(i-U) % len(p)] * pExact

        # calculate probability (when overshoot) 
        over = p[(i-U-1) % len(p)] * pOvershoot

        # calculate probability (when undershoot)
        under = p[(i-U+1) % len(p)] * pUndershoot

        # add to the list
        q.append(under + exact + over)
    return q

# update the belief
for index, Z in enumerate(measurements):
    p = sense(p, measurements[index])
    p = move(p, motions[index])

print(p)
