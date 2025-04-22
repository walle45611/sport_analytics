from app import db
from datetime import date

class EvaluationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    eval_date = db.Column(db.Date, default=date.today)

    training_status = db.Column(db.String(10))  # 😆😀🙂☹️😭
    fitness = db.Column(db.String(10))          # 體能狀況
    sleep = db.Column(db.String(10))            # 睡眠狀況
    appetite = db.Column(db.String(10))         # 食慾狀況
    note = db.Column(db.Text)                   # 備註
