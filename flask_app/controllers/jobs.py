from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import  user, job




@app.route("/jobs")    
def all_jobs_page():
    if "user_id" not in session:  
        return redirect("/")        
    data = {
        "id" :session["user_id"], 
    }
    return render_template("all_jobs.html",  this_user = user.User.get_user_by_id(data), all_jobs = job.Job.get_all_jobs(), one_user_list = user.User.get_all_user_jobs(data)) 




@app.route("/jobs/new")
def new_job_page():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : session["user_id"],
    }
    return render_template("add_job.html", this_user = user.User.get_user_by_id(data))


@app.route("/jobs/<int:id>/edit")
def edit_job_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" :id
    }
    user_data = {
        "id" : session["user_id"],
    }
    return render_template("edit_job.html", this_user = user.User.get_user_by_id(user_data), this_job = job.Job.get_one_job(data))     


@app.route("/jobs/<int:id>/view")
def view_job_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id,
    }
    return render_template("view_job.html", this_job = job.Job.get_one_job(data))  




@app.route("/jobs/add_to_db", methods = ["POST"])
def add_job_to_db():
    if "user_id" not in session:
        return redirect("/")
    if not job.Job.validate_job(request.form): 
        return redirect("/jobs/new")
    data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "location" : request.form["location"],
        "user_id" : session["user_id"]
    }
    job.Job.add_job(data) 
    return redirect("/jobs")



@app.route("/jobs/<int:id>/edit_in_db", methods = ["POST"])
def edit_job_in_db(id):
    if "user_id" not in session:
            return redirect("/")
    if not job.Job.validate_job(request.form):
        return redirect(f"/jobs/{id}/edit")
    data = {
        "job_name" : request.form["job_name"],
        "music_genre" : request.form["music_genre"],
        "home_city" : request.form["home_city"],
        "id" : id
    }  
    job.Job.update_job(data)
    return redirect("/jobs")


@app.route("/jobs/<int:id>/delete_in_db", methods = ["POST"])
def delete_from_db(id):
    if "user_id" not in session:
        return redirect(f"/jobs/{id}/delete")
    data = {
        "id" :id,
    }  
    job.Job.delete_job(data)
    return redirect("/jobs")
    


@app.route("/jobs/<int:id>/cancel")
def delete_job_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id,
    }
    job.Job.delete_job(data)
    return redirect("/jobs")


@app.route("/jobs/<int:id>/done")
def finished_job(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id,
    }
    job.Job.delete_job(data)
    return redirect("/jobs")


@app.route("/jobs/<int:job_id>/add_pro")
def add_pro(job_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "pro_id" : session["user_id"],
        "job_id" : job_id
    }
    job.Job.add_pro(data)
    return redirect("/jobs")





