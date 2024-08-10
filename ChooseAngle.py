
from AngleDef import angles_org
# In this file the therapist will choose the exercise and then store its video
def ask_exercise():
    name = input("Enter the exercise name: ")
    return name
def ask_count():
    c= int(input("How many angles do you need: "))
    return c
def make_angle(exercise_name, count, angles_int):
    choose_angle = {}
    for i in range(count):
        # Ensure angles_int has at least i+1 elements
        if i < len(angles_int):
            angle_key = angles_int[i]
            if angle_key in angles_org:
                angle_data = angles_org[angle_key]
                choose_angle[angle_key] = angle_data
                print(f"Angle {i+1}: {angle_data}")
            else:
                print(f"Angle {i+1}: Not found in angles_org")
        else:
            print(f"Angle {i+1}: Index out of range in angles_int")
    return choose_angle

    
def make_result(choose_angle):
    result = [key_point for key_point , angle_number in choose_angle.items()]
    return result



# Make a table in SQL using angle_number, angles, video_path as columns 1, 2 and 3



"""exercise_name= "Leg Raises"
choose_angle = {2: ['LEFT_ELBOW', ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST']], 4: ['RIGHT_ELBOW', ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST']], 6: ['LEFT_HIP', ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE']]}
result = [key_point for key_point , angle_number in choose_angle.items()]"""