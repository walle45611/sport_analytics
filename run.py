from app import create_app,db
from flask_migrate import Migrate

app = create_app()

# 加上這段看所有路由
print("📍 所有可用路由：")
for rule in app.url_map.iter_rules():
    print(rule)

app = create_app()
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)


