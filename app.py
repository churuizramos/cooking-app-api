from flask import Flask, request, jsonify
import pymysql  # Use pymysql if preferred
from db_config import db_host,db_user,db_password,db_database

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_database
}

# Establish MySQL connection
def get_db_connection():
    return pymysql.connect(**db_config)

# Route to insert data
@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        # Parse incoming JSON request
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        userId = data.get('userId')
        created = data.get('created')
        prepTime = data.get('prepTime')
        cookTime = data.get('cookTime')
        recyield = data.get('recyield')
        season = data.get('season')
        timeofmeal = data.get('timeofmeal')
        mealType = data.get('mealType')
        countryOfOrigin = data.get('countryOfOrigin')

        # Validate data
        if not all([title, userId, created, prepTime, cookTime, recyield]):
            return jsonify({"error": "Missing fields"}), 400

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert query
        query = "INSERT INTO Recipes (title, description, userId, created, prepTime, cookTime, yield, mealType, countryOfOrigin, season, timetoeat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, description, userId, created, prepTime, cookTime, recyield, mealType, countryOfOrigin, season, timeofmeal))
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
