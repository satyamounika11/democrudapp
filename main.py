import logging

from flask import Flask, request,render_template
import datetime
import decimal
import pymysql
import json
import config
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)

"""
CORS function is to avoid No 'Access-Control-Allow-Origin' error
"""
CORS(app)

def type_handler(x):
    """type Serialization function.

    Args:
        x:

    Returns:
        Serialization format of data, add more isinstance(x,type) if needed
    """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return '$%.2f'%(x)
    raise TypeError("Unknown type")

def rows_to_json(cols,rows):
    """type Serialization function.
    Args:
        cols: column descriptions
        rows: sql query result rows

    Returns:
        Array of json string with combination of columns and rows
        [
          {"column0":row[0], "column1":row[1], "column2":row[2], .......},
          {"column0":row[0], "column1":row[1], "column2":row[2], .......},
          {"column0":row[0], "column1":row[1], "column2":row[2], .......},
          {"column0":row[0], "column1":row[1], "column2":row[2], .......},
          {"column0":row[0], "column1":row[1], "column2":row[2], .......}
        ]
    """
    result = []
    for row in rows:
        data = dict(zip(cols, row))
        result.append(data)
    return json.dumps(result, default=type_handler)


@app.route('/')
def index():
    """webserice test method
    """
    # create mysql connection
    conn = MySQLdb.connect(host=config._DB_CONF['host'], 
                           port=config._DB_CONF['port'], 
                           user=config._DB_CONF['user'], 
                           passwd=config._DB_CONF['passwd'], 
                           db=config._DB_CONF['db'])
    
    cur = conn.cursor (MySQLdb.cursors.DictCursor)
    sql="select * from persons;"
    cur.execute(sql)
    
    # get all column names
    columns = [desc[0] for desc in cur.description]
    # get all data
    rows=cur.fetchall()
    
    cur.close()
    conn.close()

    return render_template('index.html',headers=columns,rows=rows)
	
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    #app.run(host='0.0.0.0', port=8080, debug=True, processes=4, threaded=True)
    app.run(port=8090,debug=True)
    #app.run(host='127.0.0.1', port=8080, debug=True)
## [END app]

