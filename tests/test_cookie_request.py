import requests


class TestCookieMethod:
    def test_cookie_method_request(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert response.status_code == 200

        cookies = response.cookies

        assert len(cookies) > 0, "cookies отсутствуют в ответе"

        print(cookies)

        assert "HomeWork" in cookies, "Cookie не найдены"
        assert cookies["HomeWork"] == "hw_value", "Неверные cookie"
