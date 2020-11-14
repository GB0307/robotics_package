from robotics_pkg.denavit_hartenberg import DHParameters


p = [[0, 0, 0, 0], 
     [1, 2, 3, 4], 
     [4, 0, 5, 0]]
T = DHParameters(p, inDegrees=Tre).get_transform(of=3, to=0)
print(T)

print(T.inverse)