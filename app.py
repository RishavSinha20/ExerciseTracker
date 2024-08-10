import os
from flask import Flask, render_template, jsonify, request, url_for, session,redirect,send_file, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
import Record as record_module
import ConnectDB
import mysql.connector
import MakeAngle
import Algorithm
import CalculateAverage
import logging
import CreateGraph
import importlib.util

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'Recordings')
CORS(app)



DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '1234',
    'database': 'videostore'
}

def get_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

@app.route("/") 
def LandingPage():
    return render_template("LandingPage.html")
@app.route('/fetch_exercises', methods=['GET'])
def fetch_exercises():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT exercisename FROM storage")
    exercises = cursor.fetchall()
    conn.close()

    exercises_with_videos = []
    for exercise in exercises:
        exercise_name = exercise[0]
        video_file = f"{exercise_name}_trainer.mp4"
        video_path = os.path.join('static', 'Recordings', exercise_name, video_file)
        if os.path.exists(video_path):
            exercises_with_videos.append(exercise_name)
    return jsonify(exercises_with_videos)
@app.route('/save_landmarks', methods=['POST'])
def save_landmarks():
    data = request.get_json()
    exercise_name = data['exerciseName']
    angles = data['angles']

    # Create the directory if it doesn't exist
    directory = os.path.join('static', 'Recordings', exercise_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the JavaScript file
    file_path = os.path.join(directory, f'{exercise_name}.js')
    with open(file_path, 'w') as file:
        file.write(f"const {exercise_name} = {angles};")

    return jsonify({'message': 'Landmarks saved successfully!'}), 200

@app.route('/save_js', methods=['POST'])
def save_js():
    data = request.get_json()
    filename = data['filename']
    content = data['content']
    exercise_name = data['exercise_name']
    directory = os.path.join('static', 'Recordings', exercise_name)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return jsonify({'message': 'File created successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to create file: {str(e)}'}), 500
@app.route("/ContactUs")
def ContactUs():
    return render_template("ContactUs.html")

@app.route("/Record")
def Record():
    return render_template("Record.html")

@app.route("/PlayGround")
def PlayGround():
    return render_template("PlayGround.html")

@app.route("/PlayGround/<exercise_name>")
def exercise_page(exercise_name):
    exercise_name = exercise_name.replace('_', ' ')
    exercise_folder = os.path.join(app.config['UPLOAD_FOLDER'], exercise_name)
    if os.path.exists(exercise_folder):
        video_files = [f for f in os.listdir(exercise_folder) if f.endswith('.mp4')]
        first_video = video_files[0] if video_files else None
    else:
        first_video = None

    return render_template("exercise_temp_temp.html", exercise_name=exercise_name, first_video=first_video)

@app.route('/Progress')
def Progress():
    return render_template("Progress.html")

@app.route('/RecordImplement')
def RecordImplement():
    return render_template("RecordImplement.html")


@app.route('/Submit', methods=['POST'])
def Submit():
    exercise_name = request.form.get('exercise_name')
    num_angles = request.form.get('num_angles')
    
    if not exercise_name or not num_angles:
        return "No exercise data found. Please submit the form first."
    
    num_angles = int(num_angles)
    points_sets = []
    for i in range(1, num_angles + 1):
        p1 = request.form.get(f'point{i}_1')
        p2 = request.form.get(f'point{i}_2')
        p3 = request.form.get(f'point{i}_3')
        if not p1 or not p2 or not p3:
            return "Incomplete exercise data. Please fill in all points."
        points_sets.append([int(p1), int(p2), int(p3)])
    
    angles = record_module.record(exercise_name, points_sets)
    nested_angles = [angles[i] for i in range(len(points_sets))]

    # Debugging output
  

    session['exercise_name'] = exercise_name
    session['num_angles'] = num_angles
    session['points_sets'] = points_sets
    session['nested_angles'] = nested_angles

    return redirect(url_for('SubmitPage'))


@app.route("/SubmitPage")
def SubmitPage():
    exercise_name = session.get('exercise_name')
    points_sets = session.get('points_sets')
    nested_angles = session.get('nested_angles')
    return render_template("Submit.html", exercise_name=exercise_name, points_sets=points_sets, nested_angles=nested_angles)

@app.route('/follow_exercise/<exercise_name>')
def follow_exercise(exercise_name):
    # Fetch the keypoints array from the database based on exercise_name
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='videostore')
    cursor = conn.cursor()
    cursor.execute("SELECT keypoints_array FROM storage WHERE exercisename = %s", (exercise_name,))
    result = cursor.fetchone()
    keypoints_array = result[0] if result else []

    # Ensure the keypoints array is a valid list
    keypoints_array = eval(keypoints_array) if isinstance(keypoints_array, str) else keypoints_array

    # Fetch the first video for the exercise
    first_video = None
    video_path = f'static/Recordings/{exercise_name}/'
    if os.path.exists(video_path):
        for file in os.listdir(video_path):
            if file.endswith('.mp4'):
                first_video = file
                break

    return render_template('follow_exercise.html', exercise_name=exercise_name, keypoints_array=keypoints_array, first_video=first_video)

@app.route("/Apply")
def Apply():
    exercise_name = session.get('exercise_name')
    num_angles = session.get('num_angles')
    points_sets = session.get('points_sets')
    
    # Debugging output
    print(f"Session Exercise Name: {exercise_name}")
    print(f"Session Number of Angles: {num_angles}")
    print(f"Session Points Sets: {points_sets}")
    
    if not exercise_name or not points_sets:
        return "No exercise data found. Please submit the form first."
    
    details = ConnectDB.db_connect_details()
    conn_cursor = ConnectDB.initialise_cursor(details)
    ConnectDB.create_table(conn_cursor)
    ConnectDB.insert_into_table(conn_cursor, exercise_name, num_angles, points_sets)

    return "Your exercise has been added"



# @app.route("/ApplyAlgorithm")
# def ApplyAlgorithm():
#     exercise_name = session.get('exercise_name')

#     if not exercise_name:
#         return "No exercise data found. Please submit the form first.", 400
    
#     # details = ConnectDB.db_connect_details()
#     # conn_cursor = ConnectDB.initialise_cursor(details)
#     nested_angles = session.get('nested_angles')
    
#     # try:
#     #     resultant_points = MakeAngle.process_video(exercise_name, conn_cursor)
#     # except ValueError as e:
#     #     logging.error(f"ValueError: {e}")
#     #     return str(e), 400
#     # except Exception as e:
#     #     logging.error(f"Unexpected error: {e}")
#     #     return "An unexpected error occurred.", 500

#     # rearranged_arr = Algorithm.rearranging_array(resultant_points)
#     # inflection_points_final = Algorithm.Algorithm(rearranged_arr)
#     # average = CalculateAverage.calculateAverage(inflection_points_final)

#     # Save the average value to a Python file
#     exercise_folder = os.path.join(app.config['UPLOAD_FOLDER'], exercise_name)
#     os.makedirs(exercise_folder, exist_ok=True)
#     average_file_path = os.path.join(exercise_folder, 'average.py')
    
#     with open(average_file_path, 'w') as f:
#         f.write(f"average = {average}\n")

#     return f"Average value saved successfully in {average_file_path}"

@app.route("/ApplyAlgorithm")
def ApplyAlgorithm():
    exercise_name = session.get("exercise_name")
    nested_angles = session.get("nested_angles")
        # Ensure the input data is not None
    if nested_angles is None:
        return jsonify({"error": "Input data is None"}), 400
    
    # Clean the input data
    cleaned_angles = Algorithm.cleanup(nested_angles)
    if cleaned_angles is None:
        return jsonify({"error": "Cleaned data is None"}), 500
    
    b = Algorithm.find_inflection_points(cleaned_angles)
    CreateGraph.createGraph(b,exercise_name)
    c = CalculateAverage.calculateAverage(b)

    exercise_folder = os.path.join(app.config['UPLOAD_FOLDER'], exercise_name)
    os.makedirs(exercise_folder,exist_ok=True)
    average_file_path = os.path.join(exercise_folder,f'{exercise_name}_min_max.py')
    with open(average_file_path, 'w') as f:
        f.write(f"min_max = {c}\n")
    return f"Average value saved successfully in {average_file_path}"


@app.route('/save_video', methods=['POST'])
def save_video():
    exercise_name = request.args.get('exercise_name')
    if 'video' not in request.files:
        return 'No video part', 400
    video = request.files['video']
    
    # Create the exercise folder path with the exercise name containing spaces
    exercise_path = os.path.join(app.config['UPLOAD_FOLDER'], exercise_name)
    os.makedirs(exercise_path, exist_ok=True)
    
    # Secure the filename to ensure it's safe to save
    video_filename = secure_filename(video.filename)
    video.save(os.path.join(exercise_path, video_filename))
    return 'Video saved successfully', 200

@app.route('/get_min_max_values', methods=['GET'])
def get_min_max_values():
    exercise_name = request.args.get('exercise_name')
    exercise_folder = os.path.join(app.config['UPLOAD_FOLDER'], exercise_name)
    min_max_file_path = os.path.join(exercise_folder, f'{exercise_name}_min_max.py')
    
    if not os.path.exists(min_max_file_path):
        return jsonify({'error': 'MinMax file not found'}), 404
    
    min_max = {}
    with open(min_max_file_path) as f:
        exec(f.read(), min_max)
    
    # Fetch keypoints array from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT keypoints FROM storage WHERE exercisename = %s", (exercise_name,))
    keypoints = cursor.fetchone()[0]
    conn.close()

    return jsonify({'minMaxValues': min_max['min_max'], 'keypoints': keypoints})


@app.route('/get_keypoints')
def get_keypoints():
    exercise_name = request.args.get('exercise_name')
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='1234',
        database='videostore'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT keypoints_array FROM storage WHERE exercise_name = %s", (exercise_name,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return jsonify({'keypoints': result['keypoints_array']})
    else:
        return jsonify({'keypoints': []}), 404


@app.route('/get_min_max/<exercise_name>', methods=['GET'])
def get_min_max(exercise_name):
    # Define the path to the min_max file
    file_path = os.path.join('static', 'Recordings', f'{exercise_name}', f'{exercise_name}_min_max.py')

    # Load the Python file as a module
    spec = importlib.util.spec_from_file_location("min_max", file_path)
    min_max_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(min_max_module)

    # Access the min_max variable
    min_max = getattr(min_max_module, 'min_max', [])

    return jsonify(min_max)
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
