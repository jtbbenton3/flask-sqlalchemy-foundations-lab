# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# --------- Routes required by the lab ---------

# GET /earthquakes/<int:id>  -> single quake or 404 with message
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake is None:
        return make_response({"message": f"Earthquake {id} not found."}, 404)

    payload = {
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year,
    }
    return make_response(payload, 200)

# GET /earthquakes/magnitude/<float:magnitude>
# -> all quakes with magnitude >= value, ordered by id ASC
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_quakes_by_magnitude(magnitude):
    quakes = (
        Earthquake.query
        .filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.id.asc())
        .all()
    )
    payload = {
        "count": len(quakes),
        "quakes": [
            {
                "id": q.id,
                "location": q.location,
                "magnitude": q.magnitude,
                "year": q.year,
            } for q in quakes
        ],
    }
    return make_response(payload, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)