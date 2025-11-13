from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email_without_at(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('missing_field', [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ])
    def test_create_user_without_required_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)

        error_message = response.content.decode("utf-8").lower()
        assert missing_field.lower() in error_message or "missing" in error_message or "required" in error_message, \
            f"Unexpected error message for missing field {missing_field}: {error_message}"

    def test_create_user_with_very_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = "V"

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = "skhdgihuwfiuhwuehgiuehiuywguiyqegaiueiugyiuwysoifuwiosjwkljsdnfkjvwhsfiuhwiuhgfuiwveghiu" \
                           "whiughfiuwghsefuiwgeseuiwiusgfiuwgwhiughfiuwghsefuiwgeseuiwiusgfiuwgwegesgegegergergererg" \
                           "whiughfiuwghsefuiwgeseuiwiusgfiuwgwhiughfiuwghsefuiwgeseuiwiusgfiuwgwegesgegegergergererg"

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"

    # В этой задаче нужно написать тест, который авторизовывается одним пользователем, но получает данные другого
    # (т.е. с другим ID). И убедиться, что в этом случае запрос также получает только username, так как мы не должны
    # видеть остальные данные чужого пользователя.

    def test_get_other_user_data_after_login(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")