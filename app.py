from flask import request
from flask.ext.api import FlaskAPI, status
import psycopg2
from psycopg2.extras import RealDictCursor
import random
import urlparse
import json


app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = 'JDas8dj123e&&@0h';

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse('postgres://dahgrmgyrvnjxh:43OOFe3S4YNQrq3Rsy6__ihdjZ@ec2-107-20-178-83.compute-1.amazonaws.com:5432/d4neua8lk9eb55')

print "\n---Starting app.py"

db = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)
print " + Opened database successfully"
cur = db.cursor(cursor_factory=RealDictCursor)

cur.execute("CREATE TABLE IF NOT EXISTS dataunits (id SERIAL PRIMARY KEY, username CHAR(20), comment CHAR(100), dataunit CHAR(256));")
print " + Table created successfully (or already existed)"
db.commit()


@app.route('/', methods=['GET','POST'])
def dataunits():
	if request.method == 'POST':
		cur.execute("INSERT INTO dataunits (username,comment,dataunit) VALUES(%s,%s,%s)", (
			str(request.data.get('username', '')),
			str(request.data.get('comment', '')),
			''.join(random.choice('0123456789abcdef') for i in range(256))
		))
		db.commit()
		cur.execute("SELECT * FROM dataunits")
		db.commit()
		return json.dumps(cur.fetchall(), indent=2), status.HTTP_201_CREATED
		
	cur.execute("SELECT * FROM dataunits")
	db.commit()
	return json.dumps(cur.fetchall(), indent=2)


@app.route("/<int:id>/", methods=['GET','DELETE'])
def dataunit_detail(id):
	if request.method == 'DELETE':
		cur.execute("DELETE FROM dataunits WHERE id=%s;",(id,))
		db.commit()
		return '', status.HTTP_204_NO_CONTENT

	# request.method == 'GET'
	cur.execute("SELECT * FROM dataunits WHERE id=%s;",(id,))
	db.commit()
	return json.dumps(cur.fetchone(), indent=2)



if __name__ == "__main__":
	app.run(debug = True)
