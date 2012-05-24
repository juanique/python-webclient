import unittest
from webclient import WebClient


class WebClientUnitTest(unittest.TestCase):

    def test_init(self):
        "It can be initialized specifying a server."

        client = WebClient("graph.facebook.com")
        self.assertEquals("graph.facebook.com", client.host)

    def test_init_secure(self):
        "It can be specified wheter the server uses https or not."

        client = WebClient("graph.facebook.com", https=True)
        self.assertTrue(client.https)

    def test_init_fromstring_secure(self):
        "Use of https can be infered from the input string."

        client = WebClient("https://graph.facebook.com")
        self.assertEquals("graph.facebook.com", client.host)
        self.assertTrue(client.https)

    def test_init_fromstring(self):
        "Use (and not use) of https can be infered from the input string."

        client = WebClient("http://graph.facebook.com")
        self.assertEquals("graph.facebook.com", client.host)
        self.assertFalse(client.https)


class WebClientUnitTestRequest(unittest.TestCase):

    def setUp(self):
        self.client = WebClient("http://localhost:3000")

    def test_get_html_status_code(self):
        "It can issue a GET request and return a status code"

        response = self.client.get("/")
        self.assertEquals(200, response.status_code)

    def test_get_html_content(self):
        "It can issue a GET request and return the page content"

        response = self.client.get("/")
        self.assertEquals("this is text", response.content)

    def test_get_json(self):
        "It automatically parses json data."

        response = self.client.get("data.json")

        self.assertEquals(response.data['name'], "coca cola")

    def test_get_data(self):
        "It passes POST data arguments thru the querystring."

        data = {"param1": "value1", "param2": "value2"}
        response = self.client.get("echo_get", data=data)

        self.assertEqual(response.data, data)

    def test_post_data_json(self):
        "It passes json POST data as the request body content."

        data = {"param1": "value1", "param2": "value2"}
        response = self.client.post("echo_post_json", data=data,
            content_type='application/json')

        self.assertEqual(response.data, data)

    def test_post_data_multipart(self):
        "It can POST multipart/form-data"

        data = {"param1": "value1", "param2": "value2"}
        response = self.client.post("echo_post_multipart", data=data,
            content_type='multipart/form-data')

        self.assertEqual(response.data, data)

    def test_post_data_multipart_file(self):
        "It can POST multipart/form-data with attached files"

        data = {"param1": "value1", "param2": "value2"}
        files = {"textfile" : "fixtures/test1.txt"}
        response = self.client.post("echo_post_files", data=data,
            files=files, content_type='multipart/form-data')

        data.update({'textfile': 'Awesome\n'})
        self.assertEqual(response.data, data)

class WebClientUnitTestAuth(unittest.TestCase):

    def test_auth(self):
        "It support basic http authentication."

        client = WebClient("http://localhost:3000")
        client.authenticate(username="Aladdin", password="open sesame")

        response = client.get("test_auth")
        self.assertEqual(response.data['username'], "Aladdin")
        self.assertEqual(response.data['password'], "open sesame")

if __name__ == '__main__':
    unittest.main()

