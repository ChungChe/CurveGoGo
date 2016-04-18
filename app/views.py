from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
	user = {'nickname': 'Shit'}
	return render_template('index.html', title = path, user=user)
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
