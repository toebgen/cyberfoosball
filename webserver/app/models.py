from app import db

# http://flask-sqlalchemy.pocoo.org/2.1/models/
# Many-to-Many Relationships for user and games
games = db.Table('games',
                 db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                 )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    games = db.relationship('Game', secondary=games,
                            backref=db.backref('games', lazy='dynamic'))

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    body = db.Column(db.String(140))
    home_defense = db.Column(db.Integer, db.ForeignKey('user.id'))
    home_offense = db.Column(db.Integer, db.ForeignKey('user.id'))
    guest_defense = db.Column(db.Integer, db.ForeignKey('user.id'))
    guest_offense = db.Column(db.Integer, db.ForeignKey('user.id'))
    home_goals = db.Column(db.Integer, unique=False)
    guest_goals = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Game %r>' % (self.body)
