import uuid
import os

from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = uuid.uuid4().bytes

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    session["result"] = ""
    return redirect(url_for("read_result"))


@app.route("/result", methods=["GET"])
def read_result():
    session["result"] = "./templates/index.html"
    # if "result" not in session:
    #     return redirect(f"{url_for('index', _anchor="upload")}")
    with open(session["result"]) as file:
        text = file.read()
    return render_template("result.html", file=text)


if __name__ == "__main__":
    app.run()
