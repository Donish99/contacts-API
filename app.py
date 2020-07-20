from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    """Creating connection with database"""
    conn = None
    try:
        conn = sqlite3.connect('contact.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/')
def index():
    return "Hello from app!"

@app.route("/display", methods=["GET", "POST"])
def display():
    """Get all the data from our database and returning them in JSON format"""

    # Create connection and setting the cursor
    conn = db_connection()
    cursor = conn.cursor()

    # If method is GET performing operations
    if request.method == "GET":
        # Query for getting all the data
        cursor = conn.execute("SELECT * FROM cont")
        # Getting the data to the python dictionary
        conts = [
            dict(id=row[0], name=row[1], number=row[2], year=row[3])
            for row in cursor.fetchall()
        ]
        if conts is not None:
            return jsonify(conts)
    return "Something went wrong", 400



@app.route("/create", methods=["GET", "POST"])
def create():
    """Inserting data to our Database"""

    # Create connection and setting the cursor
    conn = db_connection()
    cursor = conn.cursor()

    # If method is POST performing operations
    if request.method == "POST":

        # Getting data from request
        new_name = request.form.get('name')
        new_number = request.form.get('number')
        new_year = request.form.get('year')
        
        # Validating the data
        if not new_name:
            return 'missing information', 400 
        if not new_number:
            return 'missing information', 400 
        if not new_year:
            return 'missing information', 400 
        contact = cursor.execute(
        'SELECT * FROM cont WHERE number = ?', (new_number,)
        ).fetchone()
        if contact:
            return 'number for each contact must be unique'

        # Insering data to database
        sql = """INSERT INTO cont (name, number, year)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_name, new_number, new_year))
        conn.commit()
        return f"Contact created successfully", 201
    return "Something went wrong", 400


@app.route("/edit/<int:id>", methods=['PUT'])
def edit(id):
    """ Updating the content of contact by id"""

    # Create connection and setting the cursor
    conn = db_connection()
    cursor = conn.cursor()

    # Getting data from request
    name = request.form.get('name')
    number = request.form.get('number')
    year = request.form.get('year')
    contact = None

    # Validating the data
    if not name:
        name = contact[1] #rewrite of name
    if not number:
        number = contact[2] #rewrite of number
    if not year:
        year = contact[3] #rewrite of year


    # If method is PUT performing operations
    if request.method == 'PUT':
        # Cheching if the contact with the given id exists
        contact = cursor.execute(
        'SELECT * FROM cont WHERE id = ?', (id,)
        ).fetchone()
        if not contact:
            return "Contact not found", 404

        # Updating the existing data
        sql_query = """UPDATE cont
                SET name = ?,
                    number = ?,
                    year = ?
                WHERE id = ?"""
        cursor.execute(sql_query, (name, number, int(year), id))
        conn.commit()
        return 'Data updated', 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    # Create connection and setting the cursor
    conn = db_connection()
    cursor = conn.cursor()
    contact = None

    # If method is DELETE performing operations
    if request.method == 'DELETE':
        
        # Cheching if the contact with the given id exists
        contact = cursor.execute(
        'SELECT * FROM cont WHERE id = ?', (id,)
        ).fetchone()
        if not contact:
            return "Contact not found", 404

        # Deletig the existing data
        sql_query = 'DELETE FROM cont WHERE id=?'
        cursor.execute(sql_query,(id,))
        conn.commit()
        return "Contact succesifully deleted", 200
    return "Something went wrong", 400
    

        


if __name__ == "__main__":
    app.run()