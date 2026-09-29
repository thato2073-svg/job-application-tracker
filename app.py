from flask import Flask, flash, redirect, render_template, request, url_for
import database

app = Flask(__name__)
app.secret_key = "applytrack-dev"
STATUSES = ["Interested", "Applied", "Interview", "Offer", "Rejected"]

@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")
    return render_template("index.html", applications=database.get_applications(search, status),
                           stats=database.stats(), statuses=STATUSES, search=search, selected_status=status)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"].strip()
        role = request.form["role"].strip()
        if not company or not role:
            flash("Company and role are required.", "error")
            return render_template("form.html", application=None, statuses=STATUSES)
        database.add_application(company, role, request.form["status"], request.form["date_applied"],
                                 request.form.get("location", "").strip(), request.form.get("job_url", "").strip(),
                                 request.form.get("notes", "").strip())
        flash("Application added.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", application=None, statuses=STATUSES)

@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit(application_id):
    application = database.get_application(application_id)
    if not application:
        return ("Application not found", 404)
    if request.method == "POST":
        database.update_application(application_id, request.form["company"].strip(), request.form["role"].strip(),
                                    request.form["status"], request.form["date_applied"],
                                    request.form.get("location", "").strip(), request.form.get("job_url", "").strip(),
                                    request.form.get("notes", "").strip())
        flash("Application updated.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", application=application, statuses=STATUSES)

@app.post("/delete/<int:application_id>")
def delete(application_id):
    database.delete_application(application_id)
    flash("Application deleted.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    database.initialize()
    app.run(debug=True)
