from app import db

class TrainingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    jump_type = db.Column(db.String(50))
    jump_count = db.Column(db.Integer)

    run_distance = db.Column(db.Float)
    run_time = db.Column(db.String(20))

    weight_part = db.Column(db.String(50))
    weight_sets = db.Column(db.Integer)

    agility_type = db.Column(db.String(50))
    agility_note = db.Column(db.Text)

    special_focus = db.Column(db.Text)
