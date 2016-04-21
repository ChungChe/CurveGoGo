from flask import Flask, render_template, request, jsonify
import sqlite3 as db
import db_util

app = Flask(__name__)

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
	start = '2016-04-18 12:42:53'
	end = '2016-04-18 16:55:07'
	machine_list = range(1,25)
	outputList = query(start, end, machine_list)
	
	user = {'nickname': 'CurveGoGo'}
	return render_template('index.html', 
			title = path, 
			user = user, output = outputList )

@app.route('/put_data')
def get_data_from_html():
	start = request.args.get('datetime_start');
	print('start: ' + start)
	end = request.args.get('datetime_end');
	print('end: ' + end)
	machine_list = range(1, 25)
	outputList = query(start, end, machine_list)
	print('======')	
	print(outputList)	
	user = {'nickname': 'CurveGoGoGo'}
	return render_template('index.html', 
			title = "test", 
			user = user, output = outputList )

#print(request.args.getlist('mlist'));
#print('machine_list: ' + machine_list)
#	return jsonify({ "status": "success", "code": "200"});
if __name__ == '__main__':
    app.run(host='0.0.0.0')
