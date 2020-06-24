from typing import List
from abc import ABC
class Something(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

z: List[Something(x, y)]
h= Something("x", "y")
h1= Something("x1", "y1")
z.append(h)
z.append(h1)
z.append("whats up")

print(z[2])
#z.append(y)