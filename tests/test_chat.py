import unittest
import json
from urllib import response

from flask import request
from requests import Response

from tests.test_utils import *

URL = "http://localhost:5000"





class Test(unittest.TestCase):
    session_key = None

    def setUp(self):
        post_rest_call(self, f"{URL}/manage/init", expected_code=200)

    def test_01_get_users(self):
        result = get_rest_call(self, f"{URL}/users", expected_code=200)
        self.assertEqual(6,len(result))
      


    def test_02_get_user(self):
        result = get_rest_call(self, f"{URL}/users/1", expected_code=200)
        expected= {'contact_info': 'abbott@gmail.com', 'created_at': 'Sun, 01 Jan 1922 00:00:00 GMT', 'id':1, 'last_username_change':None, 'username':'Abbott'}
        self.assertEqual(expected , result)
        # self.assertEqual(result.status_code, 200)


    def test_get_communities(self):
        result = get_rest_call(self, f"{URL}/communities", expected_code=200)
        self.assertEqual(2,len(result))
        # self.assertEqual(result.status_code, 200)


    def test_get_community(self):
        result = get_rest_call(self, f"{URL}/communities/1", expected_code=200)
        expected= {'id': 1, 'name': 'Arrakis'}
        self.assertEqual(expected , result)
        # self.assertEqual(result.status_code, 200)


    def test_get_channels(self):
        result = get_rest_call(self, f"{URL}/channels", expected_code=200)
        self.assertEqual(5,len(result))
    #     self.assertEqual(result.status_code, 200)


    def test_get_channel(self):
        result = get_rest_call(self, f"{URL}/channels/1", expected_code=200)
        expected= {'community_id': 1, 'id': 1, 'name': 'Worms'}
        self.assertEqual(expected , result)
    #     self.assertEqual(result.status_code, 200)


    def test_get_messages(self):
        result = get_rest_call(self, f"{URL}/messages", expected_code=200)
        self.assertEqual(5,len(result))
    #     self.assertEqual(result.status_code, 200)


    def test_get_message(self):
        result = get_rest_call(self, f"{URL}/messages/1", expected_code=200)
        expected= {'channel_id': 2, 'community_id': 1, 'id': 1, 'is_unread': True, 'message': 'Hey Costello', 'receiver_id': 2, 'sender_id': 1, 'timestamp': 'Thu, 01 Jan 1925 00:00:00 GMT'}
        self.assertEqual(expected , result)
    #     self.assertEqual(result.status_code, 200)


    def test_get_suspensions(self):
        result = get_rest_call(self, f"{URL}/suspensions", expected_code=200)
        self.assertEqual(2,len(result))
    #     self.assertEqual(result.status_code, 200)


    def test_get_suspension(self):
        result = get_rest_call(self, f"{URL}/suspensions/4", expected_code=200)
        expected= {'suspended_until': 'Thu, 01 Jan 2060 00:00:00 GMT', 'user_id': 4}
        self.assertEqual(expected , result)
        
    

    def test_01_add_user(self):
        key = {"content-type": "application/json"}

        payload = {
            "username": "testuser1",
            "password": "testpassword",
            "contact_info": "testuser1@example.com"
        }
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=201)
        self.assertEqual(result.json()["message"], "User created successfully")

    def test_02_add_existing_user(self):
        key = {"content-type": "application/json"}
        
        # First attempt to add the user (should succeed)
        payload = {
            "username": "testuser1",
            "password": "testpassword",
            "contact_info": "testuser1@example.com"
        }
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=201)
        self.assertEqual(result.json()["message"], "User created successfully")
        
        # Second attempt to add the same user (should fail with 409)
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=409)
        self.assertEqual(result.json()["error"], "User already exists")


    def test_03_login_user(self):
        key = {"content-type": "application/json"}
        
        # Create the user
        payload = {
            "username": "testuser1",
            "password": "testpassword"
        }
        
        # Add the user
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=201)
        self.assertEqual(result.json()["message"], "User created successfully")
        
        # Login with the newly created user
        result = post_rest_call(self, f"{URL}/login", json.dumps(payload), key, expected_code=200)
        
        # Verify login and session key
        self.assertIn("session_key", result.json())  
        Test.session_key = result.json()["session_key"]



    def test_04_edit_user(self):
        # Step 1: Create a new user
        key = {"content-type": "application/json"}
        payload = {
            "username": "edit_test_user",
            "password": "editpassword",
            "contact_info": "edituser@example.com"
        }
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=201)
        self.assertEqual(result.json()["message"], "User created successfully")

        # Step 2: Login with the newly created user to obtain a session key
        login_payload = {
            "username": "edit_test_user",
            "password": "editpassword"
        }
        result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        self.assertIn("session_key", result.json())
        session_key = result.json()["session_key"]

        # Step 3: Edit the newly created user
        headers = {
            "Authorization": session_key,  
            "content-type": "application/json"
        }
        edit_payload = {
            "username": "updated_edit_test_user",
            "contact_info": "new_email@example.com"
        }
        # Assuming the newly created user has id 7
        result = put_rest_call(self, f"{URL}/users/7", json.dumps(edit_payload), headers, expected_code=200)

        # Step 4: Assert the success message
        self.assertEqual(result.json()["message"], "User updated successfully")

    def test_05_delete_user(self):
        key = {"content-type": "application/json"}

        # Step 1: Create a new user
        payload = {
            "username": "delete_test_user",
            "password": "deletepassword",
            "contact_info": "deleteuser@example.com"
        }
        result = post_rest_call(self, f"{URL}/users", json.dumps(payload), key, expected_code=201)
        self.assertEqual(result.json()["message"], "User created successfully")
        
        # Step 2: Login with the newly created user to obtain a session key
        login_payload = {
            "username": "delete_test_user",
            "password": "deletepassword"
        }
        result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        self.assertIn("session_key", result.json())
        session_key = result.json()["session_key"]

        # Step 3: Delete the newly created user
        headers = {"Authorization": session_key}  # Use the obtained session key
        result = delete_rest_call(self, f"{URL}/users/7", headers, expected_code=200)

        # Step 4: Assert the success message
        self.assertEqual(result.json()["message"], "User deleted successfully")





        # Test Direct Messages (Send, List)

    def test_06_send_dm(self):
        # Step 1: Login the user to get a session key
        key = {"content-type": "application/json"}
        login_payload = {"username": "Abbott", "password": "testpassword2"}
        
        # Send login request
        login_result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        
        # Retrieve session key from the login response
        session_key = login_result.json().get("session_key")
        self.assertIsNotNone(session_key, "Login failed, session key not returned")

        # Step 2: Send a direct message (DM)
        payload = {
            "receiver_id": 2,  # Assuming user Costello has ID 2
            "message": "Hello there!"
        }
        
        # Include session key in the headers
        headers = {"Authorization": session_key, "content-type": "application/json"}
        
        # Ensure the user ID (1) corresponds to the logged-in user (Abbott's ID)
        result = post_rest_call(self, f"{URL}/users/1/messages", json.dumps(payload), headers, expected_code=201)
        
        # Step 3: Validate that the message was sent successfully
        self.assertEqual(result.json()["message"], "Message sent successfully")


    def test_07_list_dms(self):
        key = {"content-type": "application/json"}
        login_payload = {"username": "Abbott", "password": "testpassword2"}
        
        # Send login request
        login_result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        
        # Retrieve session key from the login response
        session_key = login_result.json().get("session_key")
        self.assertIsNotNone(session_key, "Login failed, session key not returned")
        headers = {"Authorization": session_key}
        jdata= {}
        result = get_rest_call(self, f"{URL}/users/1/messages?limit=5",jdata, headers, expected_code=200)
        self.assertTrue(len(result) <= 5)  # Ensure it returns up to 5 messages

    # Test Authentication (Login, Logout)

    def test_08_login_incorrect(self):
         key = {"content-type": "application/json"}
         payload = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        # Send login request with wrong credentials
         result = post_rest_call(self, f"{URL}/login", json.dumps(payload), key, expected_code=401)
        
        # Check the status code to ensure it's 401 Unauthorized
         self.assertEqual(result.status_code, 401)
        
        # Check the error message in the response (assuming your API returns a message like this)
         expected_error_message = {"error": "Invalid username or password"}
         self.assertEqual(result.json(), expected_error_message) 


    def test_09_logout_user(self):
        # Step 1: Login the user to get a session key
        key = {"content-type": "application/json"}
        login_payload = {"username": "Abbott", "password": "testpassword2"}

        # Send login request and get session key
        login_result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        session_key = login_result.json().get("session_key")
        self.assertIsNotNone(session_key, "Login failed, session key not returned")

        # Step 2: Use the session key to logout the user
        headers = {"Authorization": session_key}  # Use the session key returned from login
        logout_result = post_rest_call(self, f"{URL}/logout", {}, headers, expected_code=200)

        # Step 3: Check the logout response
        self.assertEqual(logout_result.json()["message"], "Logout successful")


    def test_10_access_after_logout(self):
        # Step 1: Login the user to get a session key
        key = {"content-type": "application/json"}
        login_payload = {"username": "Abbott", "password": "testpassword2"}

        # Send login request
        login_result = post_rest_call(self, f"{URL}/login", json.dumps(login_payload), key, expected_code=200)
        session_key = login_result.json().get("session_key")
        self.assertIsNotNone(session_key, "Login failed, session key not returned")

        # Step 2: Logout the user to invalidate the session key
        headers = {"Authorization": session_key}
        logout_result = post_rest_call(self, f"{URL}/logout", {}, headers, expected_code=200)
        self.assertEqual(logout_result.json()["message"], "Logout successful")

        # Step 3: Attempt to access protected route after logout with the invalidated session key
        result = get_rest_call(self, f"{URL}/users/1/messages", headers, expected_code=401)

        # Step 4: Assert that the response returns an unauthorized error
        self.assertEqual(result["error"], "Unauthorized")


if __name__ == "__main__":
    unittest.main()
