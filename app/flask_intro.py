from flask import Flask, render_template

app = Flask(__name__)

#here we are routing/mapping using decorator '@' -- use it to map URL to return value
#the response to the URL is what the function returns
# @ signifies a decorator
@app.route('/')
def index():
    return 'This is the homepage'

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/test')
def test():
    return '<h2>Testing</h2>' #you can write html in here!

#now username is a variable if inside "<>"
@app.route('/profile/<username>')
def profile(username):
   return '<h2>Hey there %s<h2>' % username

#for integers you need to specify type int
@app.route('/post/<int:post_id>')
def post(post_id):
   return '<h2>Post ID is %s<h2>' % post_id

#Using HTML Templates
@app.route("/profile2/<name>")
def profile2(name):
    return render_template("profile.html",name=name)

if __name__ == "__main__":
    app.run(debug=True)
