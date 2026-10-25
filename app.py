
from flask import Flask, render_template, request, redirect, url_for
import secrets
import string

app = Flask(__name__)

# Temporary storage: short code -> original URL
url_mapping = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form.get("url", "").strip()

    if not original_url:
        return "Please enter a URL.", 400

    characters = string.ascii_letters + string.digits
    short_code = "".join(
        secrets.choice(characters) for _ in range(6)
    )

    while short_code in url_mapping:
        short_code = "".join(
            secrets.choice(characters) for _ in range(6)
        )

    url_mapping[short_code] = original_url

    short_url = url_for(
        "redirect_to_url",
        short_code=short_code,
        _external=True
    )

    return render_template(
        "result.html",
        original_url=original_url,
        short_url=short_url
    )


@app.route("/<short_code>")
def redirect_to_url(short_code):
    original_url = url_mapping.get(short_code)

    if original_url is None:
        return "Short URL not found.", 404

    return redirect(original_url)


if __name__ == "__main__":
    app.run(debug=True)

