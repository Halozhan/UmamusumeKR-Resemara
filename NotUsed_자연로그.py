import math

for i in range(1, 101, 1):
    print(i, round(((i*0.01)**(1.5*math.exp(1)))*8, 4))