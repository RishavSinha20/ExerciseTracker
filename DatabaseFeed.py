
import ConnectDatabase

# We only need to enter data in this manner hence always ensure that the insert_angle function is in the end
# Because it has the conn.close() function to close the connection between python and database properly.
details = ConnectDatabase.db_connect_details()
conn_cursor = ConnectDatabase.initialise_cursor(details)
list_for_angles_ins = ConnectDatabase.insert_into_table(conn_cursor)
ConnectDatabase.insert_angles_req(conn_cursor,list_for_angles_ins)

