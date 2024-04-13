from flask import Flask, render_template, request, redirect, url_for # url_forはcssを読み込むために必要
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, date

app = Flask(__name__)

# まずsqliteを使ったdatabaseのtodo.dbを作る
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

# db.Modelを継承?
# そしてtodo.dbの中身を定義するイメージ
class Post(db.Model):
    #カラムを定義 整数を入れる, 主キーに設定
    id = db.Column(db.Integer, primary_key=True)
    # 30文字以下でタイトルを必須指定
    title = db.Column(db.String(30), nullable=False)
    # 詳細項目
    detail = db.Column(db.String(100))
    # 締め切りを必須指定
    due = db.Column(db.DateTime, nullable=False)

# get, postを受け付けるようにする
@app.route("/", methods=["GET", "POST"])
def index():
    # GETはトップページにアクセスすると発動
    if request.method == "GET":
        # 投稿すべてを取り出す
        # Post.dueでソートして全て取り出す
        posts = Post.query.order_by(Post.due).all()
        return render_template("index.html", posts=posts, today=date.today())
    else:
        # formから送られたtitleがtitle変数に入る
        title = request.form.get("title")
        detail = request.form.get("detail")

        # ただしdueは文字型なのでキャストする
        due = request.form.get("due")
        due = datetime.strptime(due, "%Y-%m-%d")

        new_post = Post(title=title, detail=detail, due=due)

        # ﾃﾞｰﾀﾍﾞｰｽに追加
        db.session.add(new_post)
        db.session.commit()

        # トップにリダイレクト
        return redirect("/")

@app.route("/create")
def create():
    return render_template("create.html")

# そのidに属するタスクを表示
@app.route("/detail/<int:id>")
def read(id):
    # 該当するidを取得
    post = Post.query.get(id)
    return render_template("detail.html", post=post)

# タスクの編集
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    # 該当するidを取得
    post = Post.query.get(id)

    if request.method == "GET":
        # updateのページに遷移
        return render_template("update.html", post=post)
    else:
        # 変更内容を反映
        post.title = request.form.get("title")
        post.detail = request.form.get("detail")
        post.due = datetime.strptime(request.form.get("due"), "%Y-%m-%d")

        # dbに反映
        db.session.commit()

        # トップページに遷移
        return redirect("/")

# タスクの削除
@app.route("/delete/<int:id>")
def delete(id):
    # 該当するidを取得
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    # デバッグ用のコードらしい
    # app.run(debug=True)
    app.run()