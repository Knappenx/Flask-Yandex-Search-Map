# Flask-Yandex-Search-Map
## Description
Develop a Flask Blueprint to find the distance from the Moscow Ring Road to the specified address. The address is passed to the application in an HTTP request, if the specified address is located inside the MKAD, the distance does not need to be calculated. Add the result to the .log file

## Table of Contents (Optional)
If your README is long, add a table of contents to make it easy for users to find what they need.
- [Requirements](#requirements)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Credits](#credits)
- [Licence](#license)

## Requirements
Requirements:
1. The address is transmitted via an HTTP request
2. The functions and algorithms used are provided with informative comments
3. The tests are arranged in a separate file
4. Documentation in the form of readme.md the file contains instructions for using the application
5. PEP8 code compliance and use of type annotations

## Technologies
Project was created with:
* Python 3.8.10
* Flask 2.0.1
* Yandex GeoCoder free API

## Setup
In a Terminal, located in our project's folder we're going to create a virtual environment:
```
virtualenv venv
```
After creating it, we will proceed to activate it.
Linux/Mac:
```
source venv/bin/activate
```
Windows:
```
venv/Scripts/activate
```
Once our virtuel environment is active we will install Flask:
```
pip install flask
```
On the main folder it will be necessary to create a config.py file in which we will enter our API and Flask Secret keys as follows:
```
API_KEY = "Your_API_KEY"
SECRET_KEY = "Your_Secret_Key"
```
To run the project we execute the following command:
```
python main.py
```

## Usage
The use of the application is simple.

The main site shows a Yandex map with Moscow's Ring Road (MKAD) marked in blue, followed by an Input box and Search button.

The application finds locations or an address with 4 tested possible scenarios:
* Empty string: Asks the user to enter a location
* Invalid locations: If the location entered is not valid, will prompt that the location didn't give any results.
* Location within MKAD: Pin in red color showing the desired location.
* Location outise MKAD: Pin in blue color showing the desired location with the distance in Km to the MKAD. 

## Credits
Followed freeCodeCamp.org Flask Tutorial at: 
* https://www.youtube.com/watch?v=Z1RJmh_OqeA

Formulas for distance calculation on Earth obtained from:
* https://www.codegrepper.com/code-examples/
* https://stackoverflow.com/questions/44743075/

## License
MIT License

Copyright (c) [2021 [Xavier Nahim Abugannam Monteagudo]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
