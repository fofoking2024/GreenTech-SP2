from extensions import db


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)  # individual / company


class Company(db.Model):
    __tablename__ = "company"

    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    registration_no = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Request(db.Model):
    __tablename__ = "request"

    request_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"), nullable=False)
    point_id = db.Column(db.Integer, db.ForeignKey("collectionpoint.point_id"), nullable=False)

    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    # AI analysis fields
    ai_summary = db.Column(db.Text, nullable=True)  # short AI-generated summary of device issue
    ai_conversation = db.Column(db.Text, nullable=True)  # optional full conversation JSON
    # Location fields for user-provided coordinates
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=True)

    collection_point = db.relationship("CollectionPoint", backref="requests")


class Device(db.Model):
    __tablename__ = "device"

    device_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50))
    request_id = db.Column(db.Integer, db.ForeignKey("request.request_id"), nullable=False)


class CollectionPoint(db.Model):
    __tablename__ = "collectionpoint"

    point_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


class RequestHistory(db.Model):
    __tablename__ = "request_history"

    history_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(
        db.Integer,
        db.ForeignKey("request.request_id"),
        nullable=False
    )
    status = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)