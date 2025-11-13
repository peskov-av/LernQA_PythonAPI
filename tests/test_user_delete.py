import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    @allure.description("Test attempt to delete protected user with ID 2")
    def test_delete_user_id_2(self):
        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Try to delete user with ID 2
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected error message when trying to delete protected user"
        )

    @allure.description("Positive test for deleting newly created user")
    def test_delete_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data['email']
        password = register_data['password']

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Delete
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # Trying to get the data of a remote user
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", f"Unexpected response: {response4.text}"

    @allure.description("Negative test: attempt to delete another user while authorized as different user")
    def test_delete_user_as_another_user(self):
        # Register user 1
        user1_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=user1_data)
        Assertions.assert_code_status(response1, 200)
        user1_id = self.get_json_value(response1, "id")

        # Register user 2
        user2_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=user2_data)
        Assertions.assert_code_status(response2, 200)
        user2_id = self.get_json_value(response2, "id")

        # Login user 2
        login_data = {
            'email': user2_data['email'],
            'password': user2_data['password']
        }

        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Try delete user 1
        response4 = MyRequests.delete(
            f"/user/{user1_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        login_data_user1 = {
            'email': user1_data['email'],
            'password': user1_data['password']
        }

        response5 = MyRequests.post("/user/login", data=login_data_user1)
        auth_sid_user1 = self.get_cookie(response5, "auth_sid")
        token_user1 = self.get_header(response5, "x-csrf-token")

        response6 = MyRequests.get(
            f"/user/{user1_id}",
            headers={"x-csrf-token": token_user1},
            cookies={"auth_sid": auth_sid_user1}
        )

        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_has_key(response6, "id")
        Assertions.assert_json_value_by_name(
            response6,
            "id",
            user1_id,
            "First user was unexpectedly deleted"
        )

        # Delete user 2
        response7 = MyRequests.get(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response7, 404)
        assert response7.text == "User not found", f"Unexpected response: {response7.text}"

        response8 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response8, 400)
        assert response8.text == "Invalid username/password supplied", f"Unexpected response: {response8.text}"
