from flask import Flask, render_template_string, request, send_file
from pathlib import Path
import zipfile
import random
import string

app = Flask(__name__)

UPLOADS = Path("uploads")
UPLOADS.mkdir(exist_ok=True)

codes = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FolderShare</title>
</head>
<body>
    <h1>FolderShare</h1>

    <h2>Upload folder</h2>

    /upload
        <input type="file" name="files" webkitdirectory directory multiple>
        <button type="submit">Upload</button>
    </form>

    <hr>

    <h2>Download via code</h2>

    /get
        <input type="text" name="code" placeholder="AB12CD">
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

def generate_code():
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("files")

    code = generate_code()

    zip_path = UPLOADS / f"{code}.zip"

    with zipfile.ZipFile(zip_path, "w") as z:

        for file in files:

            if file.filename:

                temp = UPLOADS / Path(file.filename).name

                file.save(temp)

                z.write(temp, arcname=file.filename)

                temp.unlink()

    codes[code] = zip_path

    return f"""
    <h1>Upload voltooid</h1>
    <h2>Share code:</h2>
    <h1>{code}</h1>

    <p>Stuur deze code naar je vriend.</p>

    /Terug</a>
    """

@app.route("/get")
def get_file():

    code = request.args.get("code", "")

    if code not in codes:
        return "Code niet gevonden"

    return send_file(
        codes[code],
        as_attachment=True
    )

if __name__ == "__main__":
    app.run()
