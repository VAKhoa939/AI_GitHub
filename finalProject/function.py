import time
import math
import random
import msvcrt


def create_level_random(size, size1):
    arr = []
    temp = []
    for i in range (0, size):
        temp = []
        for j in range (0, size1):
            a = random.randint(0,9)
            temp.append(a)
        arr.append(temp)
    return arr


def create_matrix():
    arr = []
    temp = []
    for i in range (0, 34):
        temp = []
        for j in range (0, 30):
            a = random.randint(0,9)
            if a <= 7:
                b = random.randint(0,2)
            else: 
                b = random.randint(3, 9)
            temp.append(b)
        arr.append(temp)
    return arr


def slide_arr(arr):
    i = 0
    len1 = len(arr)
    while i < len1:
        if i != 0 and arr[i] == arr[i-1]:
            del arr[i]
            len1 = len(arr)
        else:
            i += 1   
            
                        
# create Gif function
# output_file = 'player_animation.gif'
# frame_duration = 0.5  # 100 milliseconds per frame (10 frames per second)

# # Create the animated GIF
# player_imgs[0].save(
#     output_file,
#     save_all = True,
#     append_images=player_imgs[1:],
#     duration=frame_duration
#     loop=0 
# )

def goal_point(A):
    goal = 0
    for i in range (len(A)):
        for j in range (len(A[i])):
            if A[i][j] == 1 :
                goal += 10
            if A[i][j] ==  2:
                goal += 50
    return goal
                