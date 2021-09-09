'''
@project Yandex API distance calculator
@author Xavier Nahim Abugannam Monteagudo
@date 2021-07-25
@brief:
    Develop a Flask Blueprint to find the distance from the Moscow Ring Road to
    the specified address.
    The address is passed to the application in an HTTP request, if the
    specified address is located inside the MKAD, the distance does not need to
    be calculated.
    Add the result to the .log file.
'''
# Flask imports
from flask import Flask
from flask import redirect

# Import Blueprint
from route_calc.app import mkad_route
# Import Keys
import config

main_app = Flask(__name__)
# Defining Blueprint and secret key
main_app.register_blueprint(mkad_route, url_prefix="/route")
main_app.secret_key = config.SECRET_KEY


@main_app.route("/")
def index():
    '''
    @function index()
    @brief Works as the main view for the website.

    @return Redirects to mkad_route blueprint.
    '''
    return redirect('/route')

if __name__ == "__main__":
    main_app.run(debug=True)
