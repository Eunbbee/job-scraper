from extractors.wwr import extract_wwr_jobs
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web_jobs
from export import save_to_file
from flask import Flask, render_template, request, redirect, send_file

app = Flask("JobScraper")

db = {
}


@app.route("/")
def home():
    return render_template("home.html", name="eb")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = extract_wwr_jobs(keyword) + \
            extract_berlin_jobs(keyword) + \
            extract_web_jobs(keyword)
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if not keyword:
        return redirect("/")

    jobs = db.get(keyword)
    if not jobs:
        return redirect(f"/search?keyword={keyword}")

    file_name = f"{keyword}_jobs"
    save_to_file(file_name, jobs)

    return send_file(
        f"{file_name}.csv",
        as_attachment=True
    )


app.run(debug=True)
