import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description(
        "Attempt to update user data without authorization. "
        "Expected: Request should be rejected with proper error response."
    )
    def test_try_update_user_data_while_unauthorized(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # Edit
        new_name = "Changed Name"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)

    @allure.description(
        "Attempt to update user data while authorized as different user. "
        "Expected: Operation should be forbidden due to authorization mismatch."
    )
    def test_edit_user_as_another_user(self):
        # Register user 1
        user1_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=user1_data)
        Assertions.assert_code_status(response1, 200)
        user1_id = self.get_json_value(response1, "id")

        # Register user 2
        user2_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=user2_data)
        Assertions.assert_code_status(response2, 200)

        # Login user 2
        login_data = {
            'email': user2_data['email'],
            'password': user2_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Edit user 1
        new_name = "Edit Name"
        response4 = MyRequests.put(
            f"/user/{user1_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response4, 400)

    @allure.description(
        "Attempt to update user email with invalid format (missing @ symbol) "
        "while authorized as same user. Expected: Validation should fail with error."
    )
    def test_edit_user_email_without_at_symbol(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit email
        invalid_email = "invalidemail.example.com"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )

        Assertions.assert_code_status(response3, 400)

    @allure.description(
        "Attempt to update user firstName with very short value (1 character) "
        "while authorized as same user. Expected: Validation should fail for minimum length requirement."
    )
    def test_edit_user_firstname_too_short(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit firstName
        short_name = "A"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )

        Assertions.assert_code_status(response3, 400)
