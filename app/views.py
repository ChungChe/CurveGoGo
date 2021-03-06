from flask import Flask, render_template, request, jsonify, Response, json 
import gevent
from gevent.wsgi import WSGIServer
from collections import OrderedDict
import json
import sqlite3 as db
import db_util
import flask_compress
import time

app = Flask(__name__)
flask_compress.Compress(app)

app.config['PROPAGATE_EXCEPTIONS'] = True

def query(start, end, machine_list):
    
    try:
        con = db.connect('/Users/duntex/curve/app/curve.db')
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
    '''
    machine_list = my_json.get('mlist')
    outputList = query(start, end, machine_list)
    print(machine_list)
    my_dict = []
    print('total result: ' + str(len(outputList)))
    for element in outputList:
        my_dict.append(OrderedDict([("datetime", element[2]), ("M" + str(element[0]), format(float(element[1]), '.2f'))]))
    '''

    '''
    # new format
    datetime: "str"
    value: "12.09"
    '''
    t1 = time.clock()
    outputList1 = query(start, end, [1])
    t2 = time.clock()
    print("Query takes: {}".format(t2 - t1))
    
    t3 = time.clock()
    names = ['datetime', 'value']
    data = []

    for ele in outputList1:
        datetime_data = ele[2]
        value_data = (format(float(ele[1]), '.2f'))
        data.append([datetime_data, value_data])

    ary = [dict(zip(names, ele)) for ele in data]
    ary1 = {'m1': ary}
    
    #my_dict1 = [OrderedDict(zip(names, elem)) for elem in data]
    t4 = time.clock()
    print("DB to dict takes: {}".format(t4 - t3))
    #return jsonify(m1=my_dict1)
    body = json.dumps(ary1)
    return Response(body, 200, mimetype = "application/json") 

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
#    app.run(host='0.0.0.0', port=8000)
