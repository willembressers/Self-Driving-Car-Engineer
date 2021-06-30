#write code that moves 1000 times and then prints the 
#resulting probability distribution.

p=[0, 1, 0, 0, 0]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
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
    
# move 1000 times, the same step
for i in range(1000):
    p = move(p, 1)

print(p)