from robotics_pkg.transform import PositionVector as PV, TransformMatrix as TM, RotationMatrix as RM
import numpy as np

def expect_error(func):
    out = 1
    try:
        out = func()
    except:
        out = None
    if out is not None:
        raise Exception("Expected an error but it did not occur")

def expect_values(*args):
    i = 0
    for arg in args:
        if arg[0] != arg[1]:
            raise Exception(f"Expected value {arg[0]} to be {arg[1]} on the argument {i}")
        i+=1



#*####################################################################################################################
#*                                                                                                                   #
#*           CONSTRUCTOR TESTING                                                                                     #
#*                                                                                                                   #
#*####################################################################################################################

##* POSITION VECTOR
p1 = [1,2,3]
p2 = [[1], [2], [3]]
p3 = np.array(p1)
p4 = np.array(p2)

v1 = PV(1,2,3, of=1)
v2 = PV(position=p1, of=2)
v3 = PV(position=p2, of=3)
v4 = PV(position=p3, of=4)
v5 = PV(position=p4, of=5)


##* ROTATION MATRICES
r1 = [[1,0,0],[0,1,0],[0,0,1]]
r2 = np.array(r1)
r3 = np.asmatrix(r1)

R1 = RM(r1)
R2 = RM(r2)
R3 = RM(r3)

#? Inverse Method
R1.inverse
R2.inverse
R3.inverse


##* TRANSFORM MATRIX
ps = [p1,p2,p3,p4,v1]
rs = [r1,r2,r3,R1]
ts = []
for p in ps:
    for r in rs:
        try:
            ts.append(TM(position=p, rotation=r))
        except:
            print(f"ERROR WITH:\n{r}\n{p}")

#? Inverse Method
for T in ts:
    T.inverse



#*####################################################################################################################
#*                                                                                                                   #
#*           MATH TESTING                                                                                            #
#*                                                                                                                   #
#*####################################################################################################################

##* POSITION VECTORS
p1 = [1,2,3]
p2 = [2,4,6]

P1 = PV(position=p1, of=1)
P2 = 2*P1
P3 = P1*2

expect_values((P1.of, 1), (P2.of, 1), (P3.of, 1), (P2, P3), (P1, p1), (P2, p2))
expect_error(lambda: P1*P2)


##* ROTATION MATRIX

r1 = np.identity(3)
r2 = [[ 1,  0,  0],
      [ 0,  0, -1],
      [ 0,  1,  0]]

R10 = RM(r1, 1, 0)
R21 = RM(r2, 2, 1)

expect_error(lambda: R21*R10)

R20 = R10*R21
expect_values((R20, r2), (R20.of, 2), (R20.to, 0))


##* TRANSFORM MATRICES

t10 =  [[1,  0,  0,  0],
        [0,  0, -1,  0],
        [0,  1,  0,  0],
        [0,  0,  0,  1]]
t21 =  [[1,  0,  0,  5],
        [0,  1,  0,  2], 
        [0,  0,  1,  3],
        [0,  0,  0,  1]]
t20 =  [[1,  0,  0,  5],
        [0,  0, -1, -3], 
        [0,  1,  0,  2],
        [0,  0,  0,  1]]

T10 = TM(transform=t10, of=1, to=0)
T21 = TM(transform=t21, of=2, to=1)

# MUST GIVE AN ERROR, WRONG OPERATION ORDER
expect_error(lambda: T21*T10)

T20 = T10*T21
expect_values((T20.of, 2), (T20.to, 0), (T20, t20))


# TODO: CREATE DENAVIT HARTENBERG UNIT TEST