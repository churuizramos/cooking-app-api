from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import pymysql  # Use pymysql if preferred
import os

app = Flask(__name__)
CORS(app)

# MySQL configuration
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE")
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
            WHERE title LIKE %s OR Users.username LIKE %s OR TimeofMeal.name LIKE %s OR Type.name LIKE %s OR Seasons.name LIKE %s
            LIMIT %s OFFSET %s;
        """

        cursor.execute(load_title_search_query, (like_query, like_query, like_query, like_query, like_query, limit, offset))
        result = cursor.fetchall()
        cards = [{"id": row[0], "title":row[1], "userId":row[2], "timetoeat":row[3], "mealType":row[4], "season":row[5], "prepTime": row[6], "cookTime":row[7]} for row in result]

        return jsonify(cards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Example accounts
@app.route('/new_user', methods=['POST'])
def insert_user():
    try:
        data = request.get_json()
        username = data.get('username')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        joinDate = data.get('joinDate')

        if not all([username, firstName, lastName, joinDate]):
            return jsonify({"error": "Missing fields"}),400
        
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO Users (username, firstName, lastName, joinDate) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (username, firstName, lastName, joinDate))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message":"User inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500

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

@app.route('/get_recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT Recipes.id, Recipes.title, Users.username AS userId, Recipes.created, TimeofMeal.name AS timetoeat, Type.name AS mealType, Seasons.name AS season, Recipes.prepTime, Recipes.cookTime, Recipes.description, Recipes.yield, Countries.name AS countryOfOrigin, Recipes.userId AS userId_id
            FROM Recipes
            JOIN Users ON Recipes.userId = Users.id
            JOIN TimeofMeal ON Recipes.timetoeat = TimeofMeal.id
            JOIN Type ON Recipes.mealType = Type.id
            JOIN Seasons ON Recipes.season = Seasons.id
            JOIN Countries ON Recipes.countryOfOrigin = Countries.id
            WHERE Recipes.id = %s;
        """

        cursor.execute(query, recipe_id)
        result = cursor.fetchall()

        if not result:
            abort(404, description="Recipe not found")

        recipe = [{"id": row[0], "title":row[1], "userId":row[2], "created":row[3], "timetoeat":row[4], "mealType":row[5], "season":row[6], "prepTime": row[7], "cookTime":row[8], "description":row[9], "recyield":row[10], "countryOfOrigin":row[11], "userId_id":row[12]} for row in result]
        return jsonify(recipe)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_user/<int:user_id>',methods=['GET'])
def get_user(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Users WHERE id = %s;"
        cursor.execute(query,user_id)
        result = cursor.fetchall()

        if not result:
            abort(404, description="User not found")
        
        user_data = [{"id":row[0], "username":row[1], "firstName":row[2], "lastName":row[3], "joinDate":row[4]} for row in result]
        return jsonify(user_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_cookbooks',methods=['GET'])
def get_cookbooks():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        limit = int(request.args.get('limit',10))
        offset = int(request.args.get('offsert',0))

        load_all_query = """
            SELECT Cookbooks.id, Cookbooks.title, Users.username as userId, Cookbooks.description, Cookbooks.created, Countries.name as countryOfOrigin, Type.name as mealType, TimeofMeal.name as timeofMeal  
            FROM Cookbooks
            JOIN Users ON Cookbooks.userId = Users.id
            JOIN Countries ON Cookbooks.countryOfOrigin = Countries.id
            JOIN Type ON Cookbooks.mealType = Type.id
            JOIN TimeofMeal ON Cookbooks.timeofMeal = TimeofMeal.id
            LIMIT %s OFFSET %s;
            """

        cursor.execute(load_all_query,(limit, offset))
        result = cursor.fetchall()
        covers = [{"id": row[0], "title":row[1],"userId":row[2], "description": row[3], "created":row[4], "countryOfOrigin":row[5], "mealType":row[6], "timeofMeal":row[7]} for row in result]
        return jsonify(covers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_cookbook/<int:cookbook_id>',methods=['GET'])
def get_cookbook(cookbook_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT Cookbooks.id, Cookbooks.title, Users.username as userid, Cookbooks.description, Cookbooks.created, Countries.name as countryOfOrigin, Type.name as mealtype, TimeofMeal.name as timeofMeal  
            FROM Cookbooks
            JOIN Users ON Cookbooks.userid = Users.id
            JOIN Countries ON Cookbooks.countryOfOrigin = Countries.id
            JOIN Type ON Cookbooks.mealtype = Type.id
            JOIN TimeofMeal ON Cookbooks.timeofMeal = TimeofMeal.id
            WHERE Cookbooks.id = %s;
            """
        cursor.execute(query, cookbook_id)
        result = cursor.fetchall()
        cookbook = [{"id": row[0], "title":row[1],"userid":row[2], "description": row[3], "created":row[4], "countryOfOrigin":row[5], "mealType":row[6], "timeofMeal":row[7]} for row in result]
        return jsonify(cookbook)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    port = int(os.getenv("PORT",5000))
    app.run(host='0.0.0.0', port=port)
