import uuid
import os
from io import BytesIO

from flask import Flask, render_template, redirect, url_for, request, session, send_file

from model.scheme_scanner import prepareModel
from alg_utils.alg_writer import constructFromImage

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = uuid.uuid4().bytes

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/", methods=["GET"])
def index():
    """
    Renders the main page and cleans up previous session results.

    Returns:
        html for main page
    """
    if "result" in session:
        os.remove(session["result"])
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Processes uploaded image files and generates algorithmic markdown.

    Returns:
        HTTP redirect to the read_result route.
    """
    file = request.files["file"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)
    constructFromImage(path, "./writtenAlgs/1.md")
    session["result"] = "./writtenAlgs/1.md"
    return redirect(url_for("read_result"))


@app.route("/result", methods=["GET"])
def read_result():
    """
    Displays the generated result from image processing.

    Returns:
        html for viewing result page
    """
    if "result" not in session:
        return redirect(f"{url_for('index', _anchor="upload")}")
    with open(session["result"]) as file:
        text = file.read()
    return render_template("result.html", file=text)


@app.route("/download", methods=["POST"])
def download_file():
    """Sends the resulting file to user for downloading

    Returns:
        Resulting file
    """
    buff = BytesIO()
    buff.write(request.form["file"].encode("utf-8"))
    buff.seek(0)
    return send_file(
        buff,
        mimetype="text/markdown",
        as_attachment=True,
        download_name=request.form["filename"]
    )


if __name__ == "__main__":
    prepareModel()
    app.run()