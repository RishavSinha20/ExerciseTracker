import mysql.connector
import os
import AngleDef
import ChooseAngle

def db_connect_details():
    host = input("Enter the host name for MYSQL connection : ")
    print("\n")

    user = input("Enter the user name")
    print("\n")

    password = input("Enter the password for this user : ")
    print("\n")

    database = input("Enter the database : ")
    print("\n")

    details = [host, user, password, database]
    return details

def initialise_cursor(details):
    conn = mysql.connector.connect(
        host=details[0],
        user=details[1],
        password=details[2],
        database=details[3]
    )
    cursor = conn.cursor()
    conn_cursor = [conn, cursor]
    return conn_cursor

def check_if_entry_present(conn_cursor, exercise_name):
    query = "SELECT exercisename FROM algoinput"
    conn_cursor[1].execute(query)
    check_list = [row[0] for row in conn_cursor[1].fetchall()]

    if exercise_name in check_list:
        return 1
    return 0

def create_table(conn_cursor):
    conn_cursor[1].execute('''
    CREATE TABLE IF NOT EXISTS algoinput (
        exercisename VARCHAR(255),
        videopath VARCHAR(255),
        angle1 TINYINT DEFAULT 0,
        angle2 TINYINT DEFAULT 0,
        angle3 TINYINT DEFAULT 0,
        angle4 TINYINT DEFAULT 0,
        angle5 TINYINT DEFAULT 0,
        angle6 TINYINT DEFAULT 0,
        angle7 TINYINT DEFAULT 0,
        angle8 TINYINT DEFAULT 0,
        angle9 TINYINT DEFAULT 0,
        angle10 TINYINT DEFAULT 0
    )
    ''')
    conn_cursor[0].commit()

def insert_into_table(conn_cursor, exercise_name, angles_int, count):
    video_path = os.path.join("static", "Recordings", exercise_name)

    choose_angle = ChooseAngle.make_angle(exercise_name, count, angles_int)
    angleno_list = ChooseAngle.make_result(choose_angle)
    
    # Debugging statement
    print(f"Angle numbers: {angleno_list}")

    if check_if_entry_present(conn_cursor, exercise_name) == 0:
        sql = "INSERT INTO algoinput (exercisename, videopath) VALUES (%s, %s)"
        val = (exercise_name, video_path)
        conn_cursor[1].execute(sql, val)
    elif check_if_entry_present(conn_cursor, exercise_name) == 1:
        print("This exercise has already been entered into the database\n")
        ans = int(input("Want to re-enter exercise details (Enter 0 for no, 1 for yes?"))
        if ans == 0:
            insert_into_table(conn_cursor, exercise_name, angles_int, count)
        if ans == 1:
            conn_cursor[1].execute('DELETE FROM algoinput WHERE exercisename = %s', (exercise_name,))
            conn_cursor[0].commit()

            insert_into_table(conn_cursor, exercise_name, angles_int, count)

    conn_cursor[0].commit()
    list_for_angles_ins = [exercise_name, angleno_list]
    return list_for_angles_ins

def insert_angles_req(conn_cursor, list_for_angles_ins):
    query = "SELECT exercisename FROM algoinput"
    conn_cursor[1].execute(query)
    check_list = [row[0] for row in conn_cursor[1].fetchall()]

    if list_for_angles_ins[0] in check_list:
        for angle_no in list_for_angles_ins[1]:
            # Debugging statement
            print(f"Updating angle: {angle_no}")
            anglesql = f"UPDATE algoinput SET angle{angle_no} = %s WHERE exercisename = %s"
            angleval = (1, list_for_angles_ins[0])
            conn_cursor[1].execute(anglesql, angleval)
    conn_cursor[0].commit()
    conn_cursor[0].close()

    print("Angles are inserted into the required exercise")

# Example usage (assuming ChooseAngle module and its methods are defined correctly):
# details = db_connect_details()
# conn_cursor = initialise_cursor(details)
# create_table(conn_cursor)
# list_for_angles_ins = insert_into_table(conn_cursor, "Push Ups", [30, 45, 60], 3)
# insert_angles_req(conn_cursor, list_for_angles_ins)
