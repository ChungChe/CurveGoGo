from flask import Flask, render_template, request, jsonify, url_for
import sqlite3 as db
import db_util

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

def query(start, end, machine_list):
	try:
		con = db.connect('curve.db')
		print('Connect to curve.db')
		cur = con.cursor()
		outputList = db_util.get_data(cur, start, end, machine_list)
	except db.Error, e:
		if con:
			con.rollback()
		print("Error %s" % e.args[0])
		sys.exit(1)
	finally:
		if cur:
			cur.close()
		if con:
			con.close()
		return outputList

@app.context_processor
def utility_processor():
	def zfill(value, digit):
		return str(value).zfill(digit)
	return dict(zfill=zfill)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
	print("home")	
	start = '2016-04-18 12:42:53'
	end = '2016-04-18 16:55:07'
	machine_list = range(1,25)
#outputList = query(start, end, machine_list)
	outputList = []	
	user = {'nickname': 'CurveGoGo'}
	return render_template('index.html', 
			title = path, 
			user = user, output = outputList )

@app.route('/draw_chart', methods = ['POST'])
def draw_chart():
	print("post")	
	json = request.json
	start = json.get('datetime_start')
	end = json.get('datetime_end')
	machine_list = json.get('mlist')
#start =''
#	end = ''
#	machine_list = []
	outputList = query(start, end, machine_list)
	print('-----------------  53 ')
	print(outputList)
	print('-----------------  55 ')
	user = {'nickname': 'CurveGoGo_1'}
	print(user)
	print('-----------------  58 ')
	data = {"aa" : start, "bb": end, "cc" : machine_list}
	return jsonify(data)
#return render_template('index.html', title = 'lalala', user = user, output = outputList)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
