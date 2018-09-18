## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

#I worked with Danielle Meyerson on this homework

import json
from flask import render_template, Flask, request
import requests

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def Welcome_to_SI():
    return 'Welcome to SI 364!'


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. 
# For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, 
# which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to 
# the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

@app.route('/movie/<movie_name>')
def get_movie(movie_name):
	base_url = "https://itunes.apple.com/search"
	params_diction = {}
	params_diction["term"] = movie_name
	params_diction["country"] = "US"
	resp = requests.get(base_url, params = params_diction)
	text = resp.text
	python_obj = json.loads(text)

	return str(python_obj)

# {
#  "resultCount":0,
#  "results": []
# }

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.	



@app.route('/question', methods=['GET', 'POST'])
def submit_q():
	return """<br><br>
<form action="/result" method='POST'>
  Enter your favorite number:<br>
  <input type="text" name="number" value=''>
  <br>
  <input type="submit" value="Submit">
</form>"""
  

@app.route('/result',methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        double = int(request.form['number']) * 2
        return 'Double your favorite number is {}'.format(double)



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.

@app.route('/problem4form', methods=['GET', 'POST'])
def form1():
	formstring =  """<br><br>
	<h1>Music Form </h1>
    <h2>Please enter your first name: </h2>
    <form action="http://localhost:5000/problem4form" method='POST'>
	<input type="text" name="first_name"> <br><br>
	<h2>Check boxes of artists you want to know some songs by: </h2>
	<input type="checkbox" name="artist1" value="Rihanna"> Tracks by Rihanna <br>
  	<input type="checkbox" name="artist2" value="Drake"> Tracks by Drake <br>
  	<input type="checkbox" name="artist3" value="Ed Sheeran"> Tracks by Ed Sheeran <br>
  	<input type="checkbox" name="artist4" value="Sam Smith"> Tracks by Sam Smith <br>
  	<input type="checkbox" name="artist5" value="Beyonce"> Tracks by Beyonce <br>
  	<input type="checkbox" name="artist6" value="Eminem"> Tracks by Eminem <br>
  	<input type="checkbox" name="artist7" value="Miley Cyrus"> Tracks by Miley Cyrus <br>
  	<input type="checkbox" name="artist7" value="Shawn Mendes"> Tracks by Shawn Mendes <br>
	<input type="submit" value="Find songs by these artists"> <br><br>
	"""

	if request.method == "POST":
		str_result = ""
		result_str_intro = ""
		for k in request.form: 
			if k == "first_name":
				first_name = request.form.get(k, "")
				result_str_intro += "<h3>{}, here are the songs for your artist(s)</h3>".format(first_name)
			if k != "first_name":
				artistName = request.form.get(k,"")
				baseurl = "https://itunes.apple.com/search?"
				param_dict = {'term': artistName, 'entity' : 'musicTrack'}
				response = requests.get(baseurl, params = param_dict).json()['results']
				songs = []
				for s in response:
					songs.append(s['trackName'])
				str_result += "Songs by <b>{}</b>: <i>{}</i><br><br>".format(artistName,songs)
		return formstring + result_str_intro + str_result #returning the original form along with input
	else:
		return formstring











if __name__ == '__main__':
    app.run()
