# Bipedal robot movement command grid

def enc_message_one(i):
    switcher={
        "4":"none,none,2002,none,none,2003,none,none,none,none\n",
        "5":"none,none,2003,none,none,2002,none,none,none,none\n",
        "6":"none,none,none,2002,none,none,2003,none,none,none\n",
        "7":"none,none,none,2003,none,none,2002,none,none,none\n",
        "8":"none,none,none,none,2002,none,none,2003,none,none\n",
        "9":"none,none,none,none,2003,none,none,2002,none,none\n"
    }
    return switcher.get(i,"Invalid command")

def enc_message_two(i):
    switcher={
        "q":"none,none,2002,none,none,none,none,none,none,none\n",
        "w":"none,none,2003,none,none,none,none,none,none,none\n",
        "e":"none,none,none,2002,none,none,none,none,none,none\n",
        "r":"none,none,none,2003,none,none,none,none,none,none\n",
        "t":"none,none,none,none,2002,none,none,none,none,none\n",
        "y":"none,none,none,none,2003,none,none,none,none,none\n",
        "a":"none,none,none,none,none,2002,none,none,none,none\n",
        "s":"none,none,none,none,none,2003,none,none,none,none\n",
        "d":"none,none,none,none,none,none,2002,none,none,none\n",
        "f":"none,none,none,none,none,none,2003,none,none,none\n",
        "g":"none,none,none,none,none,none,none,2002,none,none\n",
        "h":"none,none,none,none,none,none,none,2003,none,none\n",
        "u":"2002,none,none,none,none,none,none,none,none,none\n",
        "i":"2003,none,none,none,none,none,none,none,none,none\n",
        "z":"none,2002,none,none,none,none,none,none,none,none\n",
        "x":"none,2003,none,none,none,none,none,none,none,none\n",
        "c":"none,none,none,none,none,none,none,none,2002,none\n",
        "v":"none,none,none,none,none,none,none,none,2003,none\n",
        "b":"none,none,none,none,none,none,none,none,none,2002\n",
        "n":"none,none,none,none,none,none,none,none,none,2003\n"
    }
    return switcher.get(i,"Invalid command")

def menuOneText(l_leg_angles, r_leg_angles, l_ee_pos, r_ee_pos, sr_angles, waist_angle, encoded_command):
    print("Current left leg angles: ", l_leg_angles[0], l_leg_angles[1], l_leg_angles[2])
    print("Current right leg angles: ", r_leg_angles[0], r_leg_angles[1], r_leg_angles[2])
    print("")
    print("Left Leg End Effector position: ", l_ee_pos[0], l_ee_pos[1])
    print("Right Leg End Effector position: ", r_ee_pos[0], r_ee_pos[1])
    print("")
    print("Current rocking joints angles: ", sr_angles)
    print("Current waist joint angle: ", waist_angle)
    print("Current encoded command: ", encoded_command)
    print("")
    print("Use WASD,TFGH,IJKL,ZX,CV to move the lower body.")

