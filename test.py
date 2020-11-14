from robotics_pkg.transform import PositionVector as PV, TransformMatrix as TM, RotationMatrix as RM
import numpy as np


#*####################################################################################################################
#*                                                                                                                   #
#*           CONSTRUCTOR TESTING                                                                                     #
#*                                                                                                                   #
#*####################################################################################################################

##* Position Vector
p1 = [1,2,3]
p2 = [[1], [2], [3]]
p3 = np.array(p1)
p4 = np.array(p2)

v1 = PV(1,2,3, of=1)
v2 = PV(position=p1, of=2)
v3 = PV(position=p2, of=3)
v4 = PV(position=p3, of=4)
v5 = PV(position=p4, of=5)


##* Rotation Matrices
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


##* Transform Matrix
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



#!####################################################################################################################
#!                                                                                                                   #
#!           MATH TESTING                                                                                            #
#!                                                                                                                   #
#!####################################################################################################################