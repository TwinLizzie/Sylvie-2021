from math import pi
from trianglesolver import solve, degree
import turtle

# endeffector_z = 0.2
# endeffector_x = -0.2

# link_1 = 0.5
# link_2 = 0.5

def solveKinematics(ee_z, ee_x, lnk_1, lnk_2):
    joint_2 = 0
    side_c1 = 0
    angle_a1 = 0
    angle_a2 = 0
    angle_b1 = 0
    angle_b2 = 0
    pos = True

    if ee_x < 0:
        pos = False
        
    a,b,c,A,B,C = solve(a=ee_z, b=abs(ee_x), C=90*degree)

    side_c1 = c
    angle_a1 = A / degree
    angle_b1 = B / degree

    if side_c1 > (lnk_1 + lnk_2):
        print("Target out of reach!")
    else:
        a,b,c,A,B,C = solve(a=lnk_1, b=lnk_2, c=side_c1)

        # print("Knee angle: ", round(C / degree, 2))

        angle_a2 = A / degree
        angle_b2 = B / degree

        meta_a = (angle_a1 + angle_a2)
        meta_b = (angle_b1 + angle_b2)

        joint_2 = C / degree

        # print("Thigh angle: ", (180 - meta_b))
        # print("Foot angle: ", (180 - meta_a))
         
        # drawRadar(meta_a, meta_b, joint_2, lnk_1, lnk_2, pos)

        return [meta_a, meta_b, joint_2, pos]

def drawRadar(meta_a, meta_b, jnt_2, lnk_1, lnk_2, pos, pencol):
    board = turtle.Turtle()

    turtle.resetscreen()

    board.color(pencol)

    board.right(90) # draw base
    board.forward(20)

    if pos:
        board.left(meta_b)
        board.forward(lnk_1 * 150)

        board.right(180 - jnt_2)
        board.forward(lnk_2 * 150)

        board.left(90 - (180 - meta_a))
        board.forward(20)

    else:
        board.left((meta_a - 90))
        board.forward(lnk_1 * 150)

        board.right(180 - jnt_2)
        board.forward(lnk_2 * 150)

        board.left(meta_b)
        board.forward(20)

def getRoute(meta_a, meta_b, jnt_2, lnk_1, lnk_2, pos):
    turn1 = 0
    turn2 = 0
    turn3 = 0

    if pos:
        turn1 = meta_b
        turn2 = (180 - jnt_2)
        turn3 = (90 - (180 - meta_a))
    else:
        turn1 = (meta_a - 90)
        turn2 = (180 - jnt_2)
        turn3 = meta_b

    return [turn1, turn2, turn3]

def sinCosTan(lnk_1, lnk_2, hypo):
    a,b,c,A,B,C = solve(a=lnk_1, b=lnk_2, c=hypo)

    return[(A / degree), (B / degree), (C / degree)]

# print(solveKinematics(endeffector_z, endeffector_x, link_1, link_2))
