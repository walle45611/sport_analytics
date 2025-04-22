from app import create_app, db
from app.models import user, training  # ✅ 確保有匯入 training 模組

app = create_app()

with app.app_context():
    db.create_all()

print("✅ 資料庫初始化完成")
