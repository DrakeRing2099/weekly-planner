import os
import pickle 
import helpers

from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/planner")
def planner():
    # For printing the table
    '''Times: [[timestamp, task for monday, tuesday...], [timestamp, task for monday, tuesday...].....]'''
    times= []
    for i in range(0, 24):
        if i < 10:
            initial_time = "0" + str(i) + (":00")
        else:
            initial_time = str(i) + (":00")
        if i + 1 < 10:
            ending_time = "0" + str(i + 1) + (":00")
        else:
            ending_time = str(i + 1) + (":00")
        times.append([initial_time + "-" + ending_time, "-", "-", "-", "-", "-", "-", "-"])
    
    # Load the data into the data dictionary
    data = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    retrievedData = helpers.retrieveData()
    for i in retrievedData:
        data[i["day"]].append(i)
    
    # For sorting the tasks according to the starting time for each day
    count = 1
    for i in data:
        data[i].sort(key=lambda x: x['starting_time'])
        for j in data[i]:
            times[j["starting_time"]][count] = j["taskname"]
        count = count + 1    

     
    
        
    return render_template("planner.html", times=times)

@app.route("/todo", methods=["POST", "GET"])
def todo():
    if request.method == "POST":
        # These tasks are to be removed from the file
        checked_tasks = request.form.getlist('checked_tasks')
        helpers.checkTasks(checked_tasks)

    # Load the data into the data dictionary
    data = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
    retrievedData = helpers.retrieveData()
    for i in retrievedData:
        data[i["day"]].append(i)
    for i in data:
        data[i].sort(key=lambda x: x['starting_time'])

    return render_template("todo.html", tasks=data)

@app.route("/add_task", methods=["POST", "GET"])
def add_task():
    # If request method is post
    tasks = []
    if request.method == "POST":
        taskname = request.form.get("taskname")
        day = request.form.get("day")
        starting_time = request.form.get("starting_time")
        starting_time = int(starting_time.replace(":00", ""))
        ending_time = request.form.get("ending_time")
        ending_time = int(ending_time.replace(":00", ""))
        newData = {"taskname": taskname, "day": day, "starting_time": starting_time, "ending_time": ending_time}
        
        # Retrieves data from the file
        retrievedData = helpers.retrieveData()

        # If the data was a dictionary, then convert it into a list
        if isinstance(retrievedData, dict):
            temp = []
            temp.append(retrievedData)
            retrievedData = temp
        helpers.pushData(retrievedData, newData)
        retrievedData = helpers.retrieveData()
    
    # This is for the select options of starting and ending time.
    timestamps = []
    for i in range(0, 24):
        if i < 10:
            initial_time = "0" + str(i) + (":00")
        else:
            initial_time = str(i) + (":00")
        timestamps.append(initial_time)
    return render_template("add_task.html", timestamps=timestamps)