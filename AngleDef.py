# First we will define the mappable points into a dictionary
# points_dict= {"Left Arm" : ["LEFT_SHOULDER","LEFT_WRIST", "LEFT_PINKY","LEFT_INDEX","LEFT_THUMB"],"Right Arm" : ["RIGHT_SHOULDER","RIGHT_WRIST", "RIGHT_PINKY","RIGHT_INDEX","RIGHT_THUMB"]}
# Now we have to check all the points which are movable and an angle can be defined on them
# Store those points into the data structure and 

"""
0 - nose
1 - left eye (inner)
2 - left eye
3 - left eye (outer)
4 - right eye (inner)
5 - right eye
6 - right eye (outer)
7 - left ear
8 - right ear
9 - mouth (left)
10 - mouth (right)
11 - left shoulder
12 - right shoulder
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index
"""
angles_org = {4 : ["RIGHT_ELBOW",["RIGHT_SHOULDER","RIGHT_ELBOW","RIGHT_WRIST"]] , 3 : ["RIGHT_SHOULDER",["RIGHT_ELBOW","RIGHT_SHOULDER","RIGHT_HIP"]], 1 : ["LEFT_SHOULDER",["LEFT_ELBOW","LEFT_SHOULDER","LEFT_HIP"]], 2 : ["LEFT_ELBOW",["LEFT_SHOULDER","LEFT_ELBOW","LEFT_WRIST"]],5 : ["RIGHT_HIP",["RIGHT_SHOULDER","RIGHT_HIP","RIGHT_KNEE"]],6 : ["LEFT_HIP",["LEFT_SHOULDER","LEFT_HIP","LEFT_KNEE"]], 7:["RIGHT_KNEE",["RIGHT_HIP","RIGHT_KNEE","RIGHT_ANKLE"]],8:["LEFT_KNEE",["LEFT_HIP","LEFT_KNEE","LEFT_ANKLE"]], 9 : ["NOSE",["LEFT_EYE_OUTER","NOSE","LEFT_SHOULDER"]], 10 : ["NOSE",["RIGHT_EYE_OUTER","NOSE","RIGHT_SHOULDER"]]}
