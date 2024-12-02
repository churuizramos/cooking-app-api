from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql  # Use pymysql if preferred
from db_config import db_host,db_user,db_password,db_database

app = Flask(__name__)
CORS(app)

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
    
@app.route('/get_cards',methods=['GET'])
def get_cards():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))

        load_all_query = """
            SELECT Recipes.id, Recipes.title, Users.username AS userId, TimeofMeal.name AS timetoeat, Type.name AS mealType, Seasons.name AS season, Recipes.prepTime, Recipes.cookTime
            FROM Recipes
            JOIN Users ON Recipes.userId = Users.id
            JOIN TimeofMeal ON Recipes.timetoeat = TimeofMeal.id
            JOIN Type ON Recipes.mealType = Type.id
            JOIN Seasons ON Recipes.season = Seasons.id
            LIMIT %s OFFSET %s;
        """

        cursor.execute(load_all_query, (limit, offset))
        result = cursor.fetchall()
        cards = [{"id": row[0], "title":row[1], "userId":row[2], "timetoeat":row[3], "mealType":row[4], "season":row[5], "prepTime": row[6], "cookTime":row[7]} for row in result]

        return jsonify(cards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_cards_search', methods=['GET'])
def get_cards_search():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        search_value = str(request.args.get('search_value'))

        like_query = f"%{search_value}%"

        load_title_search_query = """
            SELECT Recipes.id, Recipes.title, Users.username AS userId, TimeofMeal.name AS timetoeat, Type.name AS mealType, Seasons.name AS season, Recipes.prepTime, Recipes.cookTime
            FROM Recipes
            JOIN Users ON Recipes.userId = Users.id
            JOIN TimeofMeal ON Recipes.timetoeat = TimeofMeal.id
            JOIN Type ON Recipes.mealType = Type.id
            JOIN Seasons ON Recipes.season = Seasons.id
            WHERE title LIKE %s OR Users.username LIKE %s
            LIMIT %s OFFSET %s;
        """

        cursor.execute(load_title_search_query, (like_query, like_query, limit, offset))
        result = cursor.fetchall()
        cards = [{"id": row[0], "title":row[1], "userId":row[2], "timetoeat":row[3], "mealType":row[4], "season":row[5], "prepTime": row[6], "cookTime":row[7]} for row in result]

        return jsonify(cards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
