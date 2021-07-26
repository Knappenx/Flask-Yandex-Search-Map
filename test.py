# Flask imports
from flask import Flask

# Import Python modules
import unittest

# Import blueprint
from route_calc.app import mkad_route

# Import Keys
import config

test_app = Flask(__name__)
test_app.secret_key = config.SECRET_KEY
test_app.register_blueprint(mkad_route, url_prefix='/')


class BluePrintTestCase(unittest.TestCase):
    '''
    @class BluePrintTestCase(unittest.TestCase)
    @brief This class allows to test multiple scenarios
            within the app.
    '''
    def test_index(self):
        '''
        @function test_index(self)
        @brief Tests that Flask was set up correctly.
        '''
        tester = test_app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_load_page(self):
        '''
        @function test_load_page(self)
        @brief Tests that main site loads properly
        '''
        tester = test_app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertTrue(b"Enter your address" in response.data)

    def test_valid_string(self):
        '''
        @function test_load_page(self)
        @brief Tests an empty request
        '''
        tester = test_app.test_client(self)
        city_string = "Moscow"
        response = tester.post(
                "/",
                data=dict(address=f"{city_string}"),
                follow_redirects=True
            )
        valid_string = f"You entered {city_string}"
        self.assertTrue(
                bytes(valid_string, 'utf-8') in response.data
            )

    def test_empty_string(self):
        '''
        @function test_load_page(self)
        @brief Tests an empty request
        '''
        tester = test_app.test_client(self)
        response = tester.post(
                "/",
                data=dict(address=""),
                follow_redirects=True
            )
        self.assertTrue(
                b"Please enter an address or location" in response.data
            )

    def test_invalid_string(self):
        '''
        @function test_load_page(self)
        @brief Tests an invalid request
        '''
        tester = test_app.test_client(self)
        response = tester.post(
                "/",
                data=dict(address="546$%$#"),
                follow_redirects=True
            )
        self.assertTrue(b"No results available" in response.data)

if __name__ == '__main__':
    unittest.main()
