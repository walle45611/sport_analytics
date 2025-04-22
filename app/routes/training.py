from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from flask_login import login_required, current_user
from app import db
from app.models.training import TrainingRecord
from datetime import datetime
from app.models.evaluation import EvaluationRecord  # ✅ 新增這行
from app.models.user import Announcement



training_bp = Blueprint('training', __name__)

@training_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_training():
    if request.method == 'POST':
        record = TrainingRecord(
            user_id=current_user.id,
            date=datetime.strptime(request.form['date'], "%Y-%m-%d").date(),

            jump_type=request.form.get('jump_type'),
            jump_count=int(request.form.get('jump_count') or 0),

            run_distance=float(request.form.get('run_distance') or 0),
            run_time=request.form.get('run_time'),

            weight_part=request.form.get('weight_part'),
            weight_sets=int(request.form.get('weight_sets') or 0),

            agility_type=request.form.get('agility_type'),
            agility_note=request.form.get('agility_note'),

            special_focus=request.form.get('special_focus')
        )
        db.session.add(record)
        db.session.commit()
        flash("✅ 訓練紀錄已成功上傳")
        return redirect(url_for('training.upload_training'))

    return render_template('upload.html')


@training_bp.route('/history')
@login_required
def training_history():
    training_records = TrainingRecord.query.filter_by(user_id=current_user.id).order_by(TrainingRecord.date.desc()).all()
    evaluation_records = EvaluationRecord.query.filter_by(user_id=current_user.id).order_by(EvaluationRecord.eval_date.desc()).all()
    return render_template('all_records.html', trainings=training_records, evaluations=evaluation_records)


# ✅ 編輯訓練紀錄
@training_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    record = TrainingRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return "無權限存取", 403

    if request.method == 'POST':
        record.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        record.time = request.form['time']
        record.heart_rate = float(request.form['heart_rate'])
        record.distance = float(request.form['distance'])
        record.menu = request.form['menu']
        db.session.commit()
        flash("✅ 訓練紀錄已更新")
        return redirect(url_for('training.training_history'))

    return render_template('edit_record.html', record=record)

# ✅ 刪除訓練紀錄
@training_bp.route('/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = TrainingRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return "無權限刪除", 403

    db.session.delete(record)
    db.session.commit()
    flash("🗑️ 已刪除一筆紀錄")
    return redirect(url_for('training.training_history'))

@training_bp.route('/api/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.all()
    data = [
        {
            'id': a.id,
            'title': a.title,
            'content': a.content
        }
        for a in announcements
    ]
    return jsonify(data), 200


@training_bp.route('/dashboard/announcement')
def athlete_announcement_page():
    return render_template('list.html')

