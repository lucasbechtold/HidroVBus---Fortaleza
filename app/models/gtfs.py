from app import db

class Agency(db.Model):
    __tablename__ = 'agencies'
    agency_id = db.Column(db.String(50), primary_key=True)
    agency_name = db.Column(db.String(100), nullable=False)
    agency_url = db.Column(db.String(255))
    agency_timezone = db.Column(db.String(50))

class Route(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.String(50), primary_key=True)
    agency_id = db.Column(db.String(50), db.ForeignKey('agencies.agency_id'))
    route_short_name = db.Column(db.String(50), nullable=False)
    route_long_name = db.Column(db.String(255), nullable=False)
    route_type = db.Column(db.Integer, default=3)  # 3 = Bus
    route_color = db.Column(db.String(6), default="00A859")

class Stop(db.Model):
    __tablename__ = 'stops'
    stop_id = db.Column(db.String(50), primary_key=True)
    stop_name = db.Column(db.String(255), nullable=False)
    stop_lat = db.Column(db.Float, nullable=False)
    stop_lon = db.Column(db.Float, nullable=False)

class Trip(db.Model):
    __tablename__ = 'trips'
    trip_id = db.Column(db.String(50), primary_key=True)
    route_id = db.Column(db.String(50), db.ForeignKey('routes.route_id'))
    service_id = db.Column(db.String(50))
    shape_id = db.Column(db.String(50))

class StopTime(db.Model):
    __tablename__ = 'stop_times'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.String(50), db.ForeignKey('trips.trip_id'))
    stop_id = db.Column(db.String(50), db.ForeignKey('stops.stop_id'))
    arrival_time = db.Column(db.String(8))
    departure_time = db.Column(db.String(8))
    stop_sequence = db.Column(db.Integer)

class Shape(db.Model):
    __tablename__ = 'shapes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shape_id = db.Column(db.String(50))
    shape_pt_lat = db.Float()
    shape_pt_lon = db.Float()
    shape_pt_sequence = db.Column(db.Integer)