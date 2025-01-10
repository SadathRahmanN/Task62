from django.db import connection

def get_db_connection():
    try:
        if not connection.is_usable():
            connection.connect()  # Establish a connection if not already open
        return connection
    except Exception as e:
        return f"Error: {str(e)}"  # Return the error message if connection fails

