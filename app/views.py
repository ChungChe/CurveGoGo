from flask import Flask, render_template, request, jsonify 
from collections import OrderedDict
import json
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
	outputList = []	
	user = {'nickname': 'CurveGoGo'}
	return render_template('index.html', 
			title = path, 
			user = user, output = outputList )

@app.route('/draw_chart', methods = ['POST'])
def draw_chart():
	print("post")	
	my_json = request.json
	start = my_json.get('datetime_start')
	end = my_json.get('datetime_end')
	machine_list = my_json.get('mlist')
	outputList = query(start, end, machine_list)
	my_dict = []
	print('total result: ' + str(len(outputList)))
	for element in outputList:
		my_dict.append(OrderedDict([("datetime", element[2]), ("M" + str(element[0]), format(float(element[1]), '.2f'))]))
	return jsonify(data=my_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
