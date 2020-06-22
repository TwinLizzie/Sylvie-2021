from math import pi
from trianglesolver import solve, degree
import turtle

board = turtle.Turtle()

endeffector_z = 0.4
endeffector_x = 0.15

link_1 = 0.5
link_2 = 0.5

joint_2 = 0

side_c1 = 0
angle_a1 = 0
angle_a2 = 0
angle_b1 = 0
angle_b2 = 0

if endeffector_x > 0:
    a,b,c,A,B,C = solve(a=endeffector_z, b=endeffector_x, C=90*degree)
    print("Side C", c)
    print("Angle A: ", round(A / degree, 2))
    print("Angle B: ", round(B / degree, 2))
    print("Angle C: ", round(C / degree, 2))

    side_c1 = c
    angle_a1 = A / degree
    angle_b1 = B / degree

    if side_c1 > (link_1 + link_2):
        print("Target out of reach!")
    else:
        a,b,c,A,B,C = solve(a=link_1, b=link_2, c=side_c1)
        print("Angle A opposide Link 1: ", round(A / degree, 2))
        print("Angle B opposide Link_2: ", round(B / degree, 2))
        print("Angle C middle joint: ", round(C / degree, 2))

        angle_a2 = A / degree
        angle_b2 = B / degree

        meta_a = (angle_a1 + angle_a2)
        meta_b = (angle_b1 + angle_b2)

        joint_2 = C / degree

        print("Thigh angle: ", (180 - meta_b))
        print("Foot angle: ", (180 - meta_a))
         
        board.right(90) # draw base
        board.forward(20)

        board.left(meta_b)
        board.forward(link_1 * 100)

        board.right(180 - joint_2)
        board.forward(link_2 * 100)

        board.left(90 - (180 - meta_a))
        board.forward(20)

        turtle.done()
else:
    a,b,c,A,B,C = solve(a=endeffector_z, b=abs(endeffector_x), C=90*degree)
    print("Side C", round(c, 2))
    print("Angle A: ", round(A / degree, 2))
    print("Angle B: ", round(B / degree, 2))
    print("Angle C: ", round(C / degree, 2))

    side_c1 = c
    angle_a1 = A / degree
    angle_b1 = B / degree

    if side_c1 > (link_1 + link_2):
        print("Target out of reach!")
    else:
        a,b,c,A,B,C = solve(a=link_1, b=link_2, c=side_c1)
        print("Angle A opposite Link 1: ", round(A / degree, 2))  
        print("Angle B opposite Link 2: ", round(B / degree, 2))
        print("Angle C middle joint: ", round(C / degree, 2))

        angle_a2 = A / degree
        angle_b2 = B / degree

        meta_a = (angle_a1 + angle_b2)
        meta_b = (angle_a2 + angle_b1)

        joint_2 = C / degree

        print("Angle_A1: ", angle_a1)
        print("Angle_A2: ", angle_a2)

        print("Angle_B1: ", angle_b1)
        print("Angle_B2: ", angle_b2)

        print("meta_a: ", meta_a)
        print("meta_b: ", meta_b)

        print("joint_2: ", round(C / degree, 2))

        board.right(90) # draw base
        board.forward(20)

        board.left((meta_a - 90))
        board.forward(link_1 * 100)

        board.right(180 - joint_2)
        board.forward(link_2 * 100)

        board.left(meta_b)
        board.forward(20)

        turtle.done()
