import os
import matplotlib.pyplot as plt
# import Algorithm
# import MakeAngle
import ChooseAngle

# # Example array of angles
# arr = MakeAngle.process_video()
# angle_arr = Algorithm.rearranging_array(arr)
# a = Algorithm.Algorithm(angle_arr)
# print(a)
# a = [[173, 167, 163, 172, 168, 178, 176, 179, 177, 178, 150, 154, 149, 150, 148, 32, 33, 32, 33, 32, 172, 179, 34, 33, 177, 172, 179, 35, 36, 178, 175, 176, 32, 34, 177, 179, 30, 130]]

def createGraph(angles,exercise_name):
    # Create the directory if it doesn't exist
    
    directory = f'static/Recordings/{exercise_name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for subarray in angles:
        # Create an array of indexes for the x-axis
        indexes = range(len(subarray))
        # Plot each subarray
        plt.plot(indexes, subarray, marker='o')  # 'o' marker is optional, it just makes the points visible

    # Set the labels and title
    plt.xlabel('Index')
    plt.ylabel('Angles')
    plt.title('Angle Plot')

    # Display the plot
    plt.savefig(os.path.join(directory, f'{exercise_name}_plot.png'), bbox_inches='tight')
    plt.show()

# a = [[179, 123, 134, 126, 128, 108, 175, 178, 153, 176, 178, 178, 175, 167, 175, 176, 167, 170, 169, 176, 6, 150, 44, 59, 38, 50, 33, 50, 29, 168, 173, 164, 169, 166, 176, 89, 90, 175, 175, 86, 158, 148, 175, 176, 176, 175, 178, 171], [103, 154, 136, 146, 138, 139, 126, 175, 174, 176, 177, 176, 132, 174, 179, 176, 179, 179, 178, 179, 164, 168, 167, 179, 178, 172, 12, 137, 93, 104, 0, 28, 10, 14, 13, 161, 104, 162, 86, 171, 58, 89, 4, 166, 160, 153, 160, 156, 163, 159, 160, 66, 166, 163, 166, 66, 69, 68, 168, 164, 65, 68, 66, 68, 67, 68, 165, 167, 165, 166, 165, 166, 62, 146, 129, 163, 164, 171, 170, 175, 173, 177, 179]]
# createGraph(a,"Leg Raises")