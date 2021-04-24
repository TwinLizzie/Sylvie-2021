from math import pi
from trianglesolver import solve, degree
import turtle

# eez = 0.5
# eex = -0.2

# lnk1 = 0.33
# lnk2 = 0.29

# eezL = 0.5625
# eezR = 0.5575

# foot_dist = 0.14

ikResult = []

# stage 1 variables

a1 = 0
b1 = 0
c1 = 0

A1 = 0
B1 = 0
C1 = 0

# stage 2 variables

a2 = 0
b2 = 0
c2 = 0

A2 = 0 
B2 = 0
C2 = 0

# stage 3 variables

meta_a = 0
meta_b = 0
meta_c = 0

def solveKinematicsSide(eez, eex, lnk1, lnk2):
    if eex < 0:
        ikResult = solveKinematicsNeg(eez, eex, lnk1, lnk2)
    else:
        ikResult = solveKinematicsPos(eez, eex, lnk1, lnk2)

    return [ikResult[0], ikResult[1], ikResult[2]]

def solveKinematicsPos(eez, eex, lnk1, lnk2):
    # stage 1
    a,b,c,A,B,C = solve(a=eez, c=abs(eex), B=90*degree)
    
    b1 = b
    A1 = A / degree
    C1 = C / degree

    # stage 2
    a,b,c,A,B,C = solve(a=lnk2, b=b1, c=lnk1)

    A2 = A / degree
    B2 = B / degree
    C2 = C / degree

    # stage 3
    meta_a = (C1 + A2)
    meta_b = (180 - B2)
    meta_c = (C2 - C1)

    # drawRadar(meta_a, meta_b, meta_c, lnk1, lnk2, "red")

    return [meta_a, meta_b, meta_c]

def solveKinematicsNeg(eez, eex, lnk1, lnk2):
    # stage 1
    a,b,c,A,B,C = solve(a=abs(eex), c=eez, B=90*degree)

    b1 = b 
    A1 = A / degree
    C1 = C / degree

    # stage 2
    a,b,c,A,B,C = solve(a=lnk2, b=b1, c=lnk1)

    A2 = A / degree
    B2 = B / degree
    C2 = C / degree

    # stage 3 
    meta_a = ((C1 + A2) - 90)
    meta_b = (180 - B2)
    meta_c = (A1 + C2)

    # drawRadar(meta_a, meta_b, meta_c, lnk1, lnk2, "red")

    return [meta_a, meta_b, meta_c]

def solveKinematicsFront(eezL, eezR, foot_dist):
    # stage 1
    a,b,c,A,B,C = solve(a=foot_dist, c=(eezR + 0.115), B=90*degree)

    b1 = b
    A1 = A / degree
    C1 = C / degree

    # stage 2
    a,b,c,A,B,C = solve(a=foot_dist, b=b1, c=(eezL + 0.115))

    A2 = A / degree
    C2 = C / degree

    # stage 3

    foot_angle = 180 - (A1 + C2)

    # drawRadarFront(foot_angle_R, foot_angle_L, eezL, eezR, foot_dist, "green")

    return foot_angle

def drawRadarSide(meta_a, meta_b, meta_c, lnk1, lnk2, pencol):
    board = turtle.Turtle()

    turtle.resetscreen()
    board.color(pencol)

    board.right(90) # draw base
    board.forward(40)

    board.left(meta_a)
    board.forward(lnk1 * 3)

    board.right(meta_b)
    board.forward(lnk2 * 3)

    board.left(meta_c)
    board.forward(40)

def drawRadarFront(foot_angle, eezL, eezR, foot_dist, pencol):
    board = turtle.Turtle()

    turtle.resetscreen()
    board.color(pencol)

    board.left(90)
    board.forward(40)

    board.left(90 - foot_angle)
    board.forward((0.115 + eezR) * 3)

    board.right(90)
    board.forward(foot_dist * 3)

    board.right(90)
    board.forward((0.115 + eezL) * 3)

    board.right(90 - foot_angle)
    board.forward(40)

# print(solveKinematics(eez, eex, lnk1, lnk2))
# print(solveKinematicsFront(eezL, eezR, foot_dist))
