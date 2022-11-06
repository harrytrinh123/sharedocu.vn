from app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)

class USER(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    UserName = db.Column(db.String)
    Password = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    Address = db.Column(db.String)

class CITY(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))

class CATEGORY(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))

class PRODUCT(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.String)
    ImageUrl = db.Column(db.String)
    Status = db.Column(db.Integer)
    Surcharge = db.Column(db.Integer)
    UserId = db.Column(db.Integer, db.ForeignKey(USER.Id))
    CategoryId = db.Column(db.Integer, db.ForeignKey(CATEGORY.Id))
    CityId = db.Column(db.Integer, db.ForeignKey(CITY.Id))