import hashlib
import secrets
from flask import *
from swen344_db_utils import *
from management import *


app = Flask(__name__)
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + hashed_password.hex()

# Function to verify password
def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_password = stored_password[32:]
    hashed_password = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return hashed_password.hex() == stored_password

# def hash_password(password):
#     return hashlib.sha512(password.encode()).hexdigest()

# Helper function to generate a secure session key
def generate_session_key():
    return secrets.token_hex(32)

# Middleware to check session key for protected routes
def authenticate_user():
    session_key = request.headers.get("Authorization")
    if session_key:
        sql = "SELECT id FROM Users WHERE session_key = %s"
        user = exec_get_one(sql, (session_key,))
        if user:
            return user[0]  # Return the user_id if valid
    return None


@app.route("/")
def home():
    return "RESTful API Project - Chat"

@app.route("/users", methods=["GET"])
def get_users():
    sql = (
        "SELECT id, username, contact_info, created_at, last_username_change FROM Users"
    )
    users = exec_get_all(sql)
    return (
        jsonify(
            [
                {
                    "id": user[0],
                    "username": user[1],
                    "contact_info": user[2],
                    "created_at": user[3],
                    "last_username_change": user[4]
                }
                for user in users
            ]
        )
    ), 200 


@app.route("/manage/init", methods=["POST"])
def initialize_database():
    """
    Endpoint to initialize and reset the database by rebuilding tables.
    This is primarily used for testing purposes.
    """
    try:
        rebuild_tables()  # Call the function to rebuild the database tables
        return jsonify({"message": "Database initialized successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Database initialization failed: {str(e)}"}), 500

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    sql = "SELECT id, username, contact_info, created_at, last_username_change FROM Users WHERE id = %s"
    user = exec_get_one(sql, (user_id,))
    if user:
        return (
            jsonify(
                {
                    "id": user[0],
                    "username": user[1],
                    "contact_info": user[2],
                    "created_at": user[3],
                    "last_username_change": user[4]
                }
            )        
        ), 200
    else:
        return jsonify({"error": "User not found"}), 404




@app.route("/communities", methods=["GET"])
def get_communities():
    sql = "SELECT id, name FROM Communities"
    communities = exec_get_all(sql)
    return (
        jsonify(
            [{"id": community[0], "name": community[1]} for community in communities]
        )
    ), 200




@app.route("/communities/<int:community_id>", methods=["GET"])
def get_community(community_id):
    sql = "SELECT id, name FROM Communities WHERE id = %s"
    community = exec_get_one(sql, (community_id,))
    if community:
        return jsonify({"id": community[0], "name": community[1]}), 200
    else:
        return jsonify({"error": "Community not found"}), 404




@app.route("/channels", methods=["GET"])
def get_channels():
    sql = "SELECT id, name, community_id FROM Channels"
    channels = exec_get_all(sql)
    return (
        jsonify(
            [
                {"id": channel[0], "name": channel[1], "community_id": channel[2]}
                for channel in channels
            ]
        )
    ), 200




@app.route("/channels/<int:channel_id>", methods=["GET"])
def get_channel(channel_id):
    sql = "SELECT id, name, community_id FROM Channels WHERE id = %s"
    channel = exec_get_one(sql, (channel_id,))
    if channel:
        return (
            jsonify({"id": channel[0], "name": channel[1], "community_id": channel[2]})
        ), 200
    else:
        return jsonify({"error": "Channel not found"}), 404




@app.route("/messages", methods=["GET"])
def get_messages():
    sql = "SELECT id, sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id FROM Messages"
    messages = exec_get_all(sql)
    return (
        jsonify(
            [
                {
                    "id": message[0],
                    "sender_id": message[1],
                    "receiver_id": message[2],
                    "message": message[3],
                    "timestamp": message[4],
                    "is_unread": message[5],
                    "community_id": message[6],
                    "channel_id": message[7]
                }
                for message in messages
            ]
        )
    ), 200




@app.route("/messages/<int:message_id>", methods=["GET"])
def get_message(message_id):
    sql = "SELECT id, sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id FROM Messages WHERE id = %s"
    message = exec_get_one(sql, (message_id,))
    if message:
        return (
            jsonify(
                {
                    "id": message[0],
                    "sender_id": message[1],
                    "receiver_id": message[2],
                    "message": message[3],
                    "timestamp": message[4],
                    "is_unread": message[5],
                    "community_id": message[6],
                    "channel_id": message[7]
                }
            )
        ), 200
    else:
        return jsonify({"error": "Message not found"}), 404




@app.route("/suspensions", methods=["GET"])
def get_suspensions():
    sql = "SELECT user_id, suspended_until FROM Suspensions"
    suspensions = exec_get_all(sql)
    return (
        jsonify(
            [
                {"user_id": suspension[0], "suspended_until": suspension[1]}
                for suspension in suspensions
            ]
        )
    ), 200

@app.route("/suspensions/<int:suspension_id>", methods=["GET"])
def get_suspension(suspension_id):
    sql = "SELECT user_id, suspended_until FROM Suspensions WHERE user_id = %s"
    suspension = exec_get_one(sql, (suspension_id,))
    if suspension:
        return (
            jsonify({"user_id": suspension[0], "suspended_until": suspension[1]})
        ), 200
    else:
        return jsonify({"error": "Suspension not found"}), 404
    
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")
    contact_info = data.get("contact_info", "")
    
    # Check for missing fields
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the user already exists in the database
    sql = "SELECT id FROM Users WHERE username = %s"
    existing_user = exec_get_one(sql, (username,))
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Hash the password and insert the new user into the database
    hashed_password = hash_password(password)
    sql = "INSERT INTO Users (username, password_hash, contact_info) VALUES (%s, %s, %s)"
    exec_commit(sql, (username, hashed_password, contact_info))
    
    return jsonify({"message": "User created successfully"}), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    # Get the session key from the headers
    session_key = request.headers.get("Authorization")
    print(f"Session key received for edit_user: {session_key}")  # Debugging line

    # Check if the session key matches the one stored for the user in the database
    sql = "SELECT session_key FROM Users WHERE id = %s"
    stored_key = exec_get_one(sql, (user_id,))
    print(f"Stored session key for user {user_id}: {stored_key}")  # Debugging line

    if stored_key and stored_key[0] == session_key:
        # Proceed with updating the user info
        # Your existing logic for updating user info here
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # Authenticate the user using the session key from the request header
    user_id_from_session = authenticate_user()
    
    # If authentication fails, return an unauthorized error
    if not user_id_from_session:
        return jsonify({"error": "Unauthorized"}), 401

    # Check if the user is trying to delete their own account
    if user_id_from_session != user_id:
        return jsonify({"error": "Forbidden: Cannot delete another user"}), 403

    # Proceed with deleting the user if authorized
    sql = "DELETE FROM Users WHERE id = %s"
    exec_commit(sql, (user_id,))

    return jsonify({"message": "User deleted successfully"}), 200


# Message-related routes
@app.route("/users/<int:user_id>/messages", methods=["GET"])
def list_dms(user_id):
    user_id_from_session = authenticate_user()
    if not user_id_from_session:
        return jsonify({"error": "Unauthorized"}), 401

    limit = request.args.get("limit", 10)
    sql = "SELECT id, sender_id, receiver_id, message, timestamp FROM Messages WHERE receiver_id = %s LIMIT %s"
    messages = exec_get_all(sql, (user_id, limit))
    return jsonify(
        [
            {
                "id": msg[0],
                "sender_id": msg[1],
                "receiver_id": msg[2],
                "message": msg[3],
                "timestamp": msg[4]
            }
            for msg in messages
        ]
    ), 200

@app.route("/users/<int:user_id>/messages", methods=["POST"])
def send_dm(user_id):
    user_id_from_session = authenticate_user()
    if not user_id_from_session:
        return jsonify({"error": "Unauthorized"}), 401

    # Ensure the user from session is the same as the user in the URL
    if user_id_from_session != user_id:
        return jsonify({"error": "Forbidden: You cannot send messages as another user"}), 403

    data = request.json
    receiver_id = data.get("receiver_id")
    message = data.get("message")
    
    if not receiver_id or not message:
        return jsonify({"error": "Receiver ID and message are required"}), 400

    sql = "INSERT INTO Messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)"
    exec_commit(sql, (user_id_from_session, receiver_id, message))
    return jsonify({"message": "Message sent successfully"}), 201

    
@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if user exists
    sql = "SELECT id, password_hash FROM Users WHERE username = %s"
    user = exec_get_one(sql, (username,))
    
    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401  # Unauthorized

    user_id, stored_password_hash = user
    print(user_id)

    # Verify the password
    if not verify_password(stored_password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401  # Unauthorized

    # Generate session key
    session_key = generate_session_key()

    # Store the session key in the database
    sql = "UPDATE Users SET session_key = %s WHERE id = %s"
    exec_commit(sql, (session_key, user_id))

    return jsonify({"session_key": session_key}), 200


@app.route("/logout", methods=["POST"])
def logout():
    # Authenticate the user using the session key from the headers
    user_id_from_session = authenticate_user()

    # If authentication fails, return an unauthorized error
    if not user_id_from_session:
        return jsonify({"error": "Unauthorized"}), 401

    # Nullify the session key for the logged-in user
    sql = "UPDATE Users SET session_key = NULL WHERE id = %s"
    exec_commit(sql, (user_id_from_session,))

    return jsonify({"message": "Logout successful"}), 200



if __name__ == "__main__":
    rebuild_tables()
    app.run(debug=True)
