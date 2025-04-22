from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, jsonify
from app import db 
from app.models.user import Announcement
from datetime import datetime
from flask import render_template, flash, redirect, url_for

coach_bp = Blueprint('coach', __name__)

@coach_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('cdashboard.html')  # ✅ 指向正確的模板


@coach_bp.route('/create_announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    if current_user.role != 'coach':
        flash('您沒有權限新增公告')
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']

        new_announcement = Announcement(
            date=datetime.strptime(date, "%Y-%m-%d"),
            title=title,
            content=content,
            category=category,
            coach_id=current_user.id
        )
        db.session.add(new_announcement)
        db.session.commit()
        flash('✅ 公告已成功發佈！')
        return redirect(url_for('coach.dashboard'))

    return render_template('create_announcement.html')

@coach_bp.route('/dashboard/announcements')
@login_required
def announcements():
    if current_user.role != 'coach':
        flash("您無權查看此頁面", "danger")
        return redirect(url_for('main.index'))

    announcements = Announcement.query.filter_by(coach_id=current_user.id).all()
    return render_template('announcements.html', announcements=announcements)


@coach_bp.route('/announcement/edit/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(_id):
    # 確保只有教練能編輯公告
    announcement = Announcement.query.get_or_404(_id)
    
    # 檢查當前用戶是否是公告的創建者
    if announcement.coach_id != current_user.id:  # 確保這個公告屬於當前教練
        flash("您無權編輯這個公告！", "danger")
        return redirect(url_for('coach.dashboard'))
    
    if request.method == 'POST':
        # 轉換表單日期為 Python 的 date 物件
        date_str = request.form['date']
        announcement.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 更新其他公告資訊
        announcement.title = request.form['title']
        announcement.content = request.form['content']
        
        db.session.commit()
        flash("公告已更新！", "success")
        return redirect(url_for('coach.dashboard'))
    
    return render_template('edit_announcement.html', announcement=announcement)

@coach_bp.route('/announcement/delete/<int:_id>', methods=['POST'])
@login_required
def delete_announcement(_id):
    # 確保只有教練能刪除自己的公告
    announcement = Announcement.query.get_or_404(_id)
    
    if announcement.coach_id != current_user.id:  # 確保這個公告屬於當前教練
        flash("您無權刪除這個公告！", "danger")
        return redirect(url_for('coach.dashboard'))

    db.session.delete(announcement)
    db.session.commit()
    flash("公告已刪除！", "success")
    return redirect(url_for('coach.dashboard'))