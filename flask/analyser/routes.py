from flask import render_template, send_file, send_from_directory, request, redirect, url_for, flash, jsonify
from analyser import app, db
from analyser.forms import NewProjectForm, SelectProjectForm, AddSessionForm, AddLogForm
from analyser.models import Project, Session, Log, Task, Set, Settings
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
import glob
import shutil
from analyser.converter import UlogConverter
from analyser.plugins import Plugins
from analyser.createPDF import PDF
from datetime import date
import time

# MODULES
#flask
#Flask-SQLAlchemy
#flask-login
#flask-wtf
#geopy
#squaternion
#fpdf




@app.route('/', methods=["GET","POST"])
def home():
    print("home")
    form = SelectProjectForm()
    projectList = [name.title for name in Project.query.all()]
    form.project_name.choices = projectList
    if form.validate_on_submit():
        name = str(form.project_name.data)
        project = Project.query.filter_by(title=name).first()
        login_user(project)
        return redirect(url_for('project'))
    return render_template('index.html', form=form)

@app.route('/settings', methods=['GET','POST'])
def settings():
    print("settings")
    curr_project = current_user.get_id()

    if request.method == 'POST':
        data = request.get_json()
        setting = Settings.query.filter_by(project_id=curr_project).first()
        if "Topics" in data.keys():
            topics = data["Topics"]
            setting.topics = json.dumps(topics)
            db.session.commit()
        elif "lightTheme" in data.keys():
            if data["lightTheme"] == "light":
                print("light selected")
                setting.color_theme = "light"
            else:
                setting.color_theme = "dark"
                print("dark selected")
            db.session.commit()

    setting = Settings.query.filter_by(project_id=curr_project).first()
    theme = "checked" if setting.color_theme == "light" else ""
    topic_list = json.loads(setting.topics)
    return render_template('settings.html', topics=topic_list, theme=theme)

@app.route('/datasettings', methods=['POST','GET'])
def datasettings():
    print("DataSettings")
    selections = request.get_json()
    type = selections["type"]
    id = selections["id"]
    reader = DataReader()
    selTopics = {}

    if type == "log":
        log = Log.query.filter_by(id=id).first()
        def_topics = json.loads(log.def_topics)
        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        (topList, fName) = getFileList(fileName, dirName)
        (namesDict, _, _) = reader.readDataNames(log.id, dirName, fName, topList, 0)
        for top in namesDict.keys():
            if top in def_topics:
                selTopics[top] = True
            else:
                selTopics[top] = False

        resp = jsonify(selTopics)
        return resp


@app.route('/savepdf', methods=['POST','GET'])
def savepdf():
    print("saving PDF...")
    data = request.get_json()
    today = date.today()
    noteCh = data["notes"]
    logCh = data["logs"]
    taskCh = data["tasks"]
    ses_id = data["ses_id"]
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.setDate(today.strftime("%d/%m/%y"))
    ses = Session.query.filter_by(id=ses_id).first()
    pdf.setSession(ses.title)
    proj = Project.query.filter_by(id=ses.project_id).first()
    pdf.setProject(proj.title)
    pdf.setCompany(proj.company)
    pdf.setEngineer(proj.engineer)
    pdf.alias_nb_pages()
    pdf.add_page()
    if noteCh:
        pdf.notes(ses.notes)
    if taskCh:
        task = Task.query.filter_by(session_id=ses_id).all()
        pdf.taskTitle()
        for t in task:
            pdf.tasks(t.title,t.result)
    if logCh:
        log = Log.query.filter_by(session_id=ses_id).all()
        pdf.logTitle()
        for l in log:
            pdf.set(l.title,l.notes, "ID: " + str(l.id) + " Filename: " + l.file_name)

        set = Set.query.filter_by(session_id=ses_id).all()
        pdf.setTitle()
        for s in set:
            pdf.set(s.title,s.notes, "Set ID: " + str(s.id) + " Log IDs: " + str(s.log))

    export_path = os.path.join(app.root_path, 'static/export/*')
    files = glob.glob(export_path)
    for f in files:
        os.remove(f)  # remove previous files
    random_hex = secrets.token_hex(8)
    pdf_path = os.path.join(app.root_path, 'static/export', random_hex + '.pdf')
    pdf.output(pdf_path, 'F')
    resp = jsonify(random_hex)
    time.sleep(0.5)
    print("PDF completed")
    return resp


@app.route('/new_project', methods=["GET","POST"])
def new_project():
    print("newProject")
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(title=str(form.project_name.data), description=str(form.project_description.data),
                          company=str(form.company.data), engineer=str(form.engineer.data))
        db.session.add(project)
        db.session.flush()
        setting = Settings(project_id=project.id, topics=json.dumps([]))
        db.session.add(setting)
        db.session.commit()
        flash(f'{form.project_name.data} Project was created!', 'success')
        return redirect(url_for('home'))

    return render_template("new_project.html", form=form)

@app.route('/new_session', methods=["GET","POST"])
def new_session():
    print("newSession")
    form = AddSessionForm()
    if form.validate_on_submit():
        ses = Session(title=str(form.title.data),
                      notes=str(form.notes.data),
                      project_id=int(current_user.get_id()))
        db.session.add(ses)
        db.session.commit()
        print("new Session has been created")
        return redirect(url_for('session', session_id=ses.id))

    return render_template("new_session.html", form=form)

@app.route('/new_log/<session>', methods=["GET","POST"])
def new_log(session):
    form = AddLogForm()
    if form.validate_on_submit():
        if form.log_file.data:

            curr_project = current_user.get_id()
            setting = Settings.query.filter_by(project_id=curr_project).first()

            for file in form.log_file.data:

                if file.filename == "":
                    flash("File selection was empty...", "warning")
                    return redirect(url_for('session', session_id=session))
                elif file.filename.split(".")[-1] != "ulg":
                    flash("Selected file format is not supported. Only .ulg files can be imported", "warning")
                    return redirect(url_for('session', session_id=session))

                (log_path, file_name) = save_file(file)

                enteredTitle = str(form.title.data)
                if enteredTitle == "":
                    enteredTitle = str(file_name)

                lg = Log(title=str(enteredTitle),
                         notes=str(form.notes.data),
                         session_id=int(session),
                         file_name=(str(file_name)),
                         dir_name=str(log_path),
                         def_topics=setting.topics,
                         defGPSCheck=int(1))
                db.session.add(lg)
                db.session.commit()

                plugin = Plugins()
                plugin.addToOneLog(file_name, log_path)

                print("Log was successfuly saved to {}".format(log_path))
        return redirect(url_for('session', session_id=session))
    return render_template("new_log.html", form=form)

@app.route('/refresh', methods=["POST"])
def refresh():
    print("refresh")
    data = request.get_json()
    if data["Type"] == "Log":
        log = Log.query.filter_by(id=data["id"]).first()
        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        (topList, fName) = getFileList(fileName, dirName)  # returns list of topic-names and filename (without .csv)

        plugin = Plugins()
        plugin.addToOneLog(fName, dirName)

        resp = jsonify(url_for('session', session_id=log.session_id))
        return resp

    elif data["Type"] == "Set":
        set = Set.query.filter_by(id=data["id"]).first()
        dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
        lg_ids = []
        for log in set.log:
            lg_ids.append(log.id)
        topic_list = json.loads(set.def_topics)
        mergedData = readAndMergeData(lg_ids, topic_list, True if (set.defGPSCheck == 1) else False)
        plugin = Plugins()
        plugin.addToMultipleLogs(mergedData, dirName, lg_ids)

        resp = jsonify(url_for('session', session_id=set.session_id))
        return resp

@app.route('/new_set/<session>', methods=["GET","POST"])
def new_set(session):
    logs = Log.query.filter_by(session_id=session).all()

    if request.method == 'POST':
        print("creating a new set...")
        sets = request.get_json()

        if (len(sets["logs"]) == 0) or (len(sets["tops"]) == 0):
            print("Nothing selected. Set was not created.")
            return jsonify(url_for('session', session_id=session))

        set_path = createSetDir()
        mergedData = readAndMergeData(sets["logs"], sets["tops"], sets["syncOnGPS"])
        plugin = Plugins()
        plugin.addToMultipleLogs(mergedData, set_path, sets["logs"])

        st = Set(title=str(sets["title"]),
                  notes=str(sets["notes"]),
                session_id=int(session),
                 dir_name=str(set_path),
                 def_topics=json.dumps(sets["tops"]),
                 defGPSCheck=int(1 if sets["syncOnGPS"] else 2))
        db.session.add(st)
        db.session.flush()
        for l in sets["logs"]:
            log = Log.query.filter_by(id=l).first()
            st.log.append(log)
        db.session.commit()
        resp = jsonify(url_for('session', session_id=session))
        return resp
    return render_template("new_set.html", logs=logs, session_id=session)

@app.route('/loadtopics', methods=["POST"])
def loadtopics():
    logs = request.get_json()
    curr_project = current_user.get_id()
    reader = DataReader()
    topArr = []
    topics = {}
    if logs["logs"] == []:
        return jsonify({'error': 'Select at least one log and press Commit again.'})
    for id in logs["logs"]:
        log = Log.query.filter_by(id=id).first()
        setting = Settings.query.filter_by(project_id=curr_project).first()
        def_topics = json.loads(setting.topics)
        if "setId" in logs.keys():
            set = Set.query.filter_by(id=logs["setId"]).first()
            def_topics = json.loads(set.def_topics)
        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        (topList, fName) = getFileList(fileName, dirName)
        (namesDict, _, _) = reader.readDataNames(log.id, dirName, fName, topList, 0)
        for key in namesDict.keys():
            if key not in topArr:
                topArr.append(key)

    for top in topArr:
        if top in def_topics:
            topics[top] = True
        else:
            topics[top] = False

    return jsonify({'success':topics, 'error': 'false'})

@app.route("/update/<session>", methods=["GET", "POST"])
def update(session):
    print("update")
    if request.method == 'POST':
        if "projTypeToUpdate" in request.form.keys():
            id = request.form["projIds"]
            title = request.form["projTitle"]
            notes = request.form["projDetail"]
            comp = request.form["company"]
            engineer = request.form["engineer"]
            project = Project.query.filter_by(id=id).first()
            project.title = title
            project.description = notes
            project.company = comp
            project.engineer = engineer
            db.session.commit()
            return redirect(url_for('project', session_id=session))

        if request.form["typeToUpdate"] == "Task":
            id = request.form["ids"]
            title = request.form["title"]
            results = request.form["detail"]
            task = Task.query.filter_by(id=id).first()
            task.title = title
            task.result = results
            db.session.commit()

        elif request.form["typeToUpdate"] == "Session":
            id = request.form["ids"]
            title = request.form["title"]
            notes = request.form["detail"]
            session = Session.query.filter_by(id=id).first()
            session.title = title
            session.notes = notes
            db.session.commit()
            session = id

        elif request.form["typeToUpdate"] == "Log":
            id = request.form["ids"]
            title = request.form["title"]
            notes = request.form["detail"]
            log = Log.query.filter_by(id=id).first()
            log.title = title
            log.notes = notes
            db.session.commit()

        elif request.form["typeToUpdate"] == "Set":
            id = request.form["ids"]
            title = request.form["title"]
            notes = request.form["detail"]
            set = Set.query.filter_by(id=id).first()
            set.title = title
            set.notes = notes
            db.session.commit()

        return redirect(url_for('session', session_id=session))

@app.route("/task_delete/<session>", methods=["GET","POST"])
def delete(session):
    print("delete")
    if request.method == 'POST':
        if "projTypeToDelete" in request.form.keys():
            id = current_user.id
            proj = Project.query.filter_by(id=id).first()
            sessions = Session.query.filter_by(project_id=id).all()
            for ses in sessions:
                logs = Log.query.filter_by(session_id=ses.id).all()
                for log in logs:
                    dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
                    if os.path.isdir(dirName):
                        shutil.rmtree(dirName)
                    db.session.delete(log)
                sets = Set.query.filter_by(session_id=ses.id).all()
                for set in sets:
                    dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
                    if os.path.isdir(dirName):
                        shutil.rmtree(dirName)
                    db.session.delete(set)
            logout_user()
            db.session.delete(proj)
            db.session.commit()
            return redirect(url_for('home'))

        if request.form["typeToDelete"] == "Task":
            id = request.form["idd"]
            Task.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('session', session_id=session))
        elif request.form["typeToDelete"] == "Session":
            id = request.form["idd"]
            session = Session.query.filter_by(id=id)
            Task.query.filter_by(session_id=id).delete()
            logs = Log.query.filter_by(session_id=id).all()
            for log in logs:
                dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
                if os.path.isdir(dirName):
                    shutil.rmtree(dirName)
                db.session.delete(log)

            sets = Set.query.filter_by(session_id=id).all()
            for set in sets:
                dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
                if os.path.isdir(dirName):
                    shutil.rmtree(dirName)
                db.session.delete(set)
            session.delete()
            db.session.commit()
            curr_project = current_user.get_id()
            sessions = Session.query.filter_by(project_id=curr_project).all()
            return redirect(url_for("project", test_sessions=sessions))
        elif request.form["typeToDelete"] == "Log":
            id = request.form["idd"]
            log = Log.query.filter_by(id=id).first()
            dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
            if os.path.isdir(dirName):
                shutil.rmtree(dirName)

            sets = Set.query.filter(Set.log.any(id=log.id)).all()
            db.session.delete(log)
            for set in sets:
                dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
                if os.path.isdir(dirName):
                    shutil.rmtree(dirName)
                db.session.delete(set)

            db.session.commit()
            return redirect(url_for('session', session_id=session))
        elif request.form["typeToDelete"] == "Set":
            id = request.form["idd"]
            set = Set.query.filter_by(id=id).first()
            dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
            if os.path.isdir(dirName):
                shutil.rmtree(dirName)
            db.session.delete(set)
            db.session.commit()
            return redirect(url_for('session', session_id=session))


@app.route('/project', methods=["GET","POST"])
@login_required
def project():
    print("project")
    curr_project = current_user.get_id()
    sessions = Session.query.filter_by(project_id=curr_project).all()
    curr_project = current_user.get_id()
    return render_template("project.html", test_sessions=sessions)

from analyser.DataReader import DataReader
import json
@app.route('/analyser2D/<type>/<id>', methods=['GET', 'POST'])
def analyser2D(type, id):
    print("analyser2D")
    reader = DataReader()
    log_ids = []
    selTopics = {}
    topics = {}
    ids = id
    gpsAvail = 0

    if type == "set":
        set = Set.query.filter_by(id=ids).first()
        session_id = set.session_id
        dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
        (namesDict, timeStamp, _) = reader.readNamesFromSet(dirName)
        def_topics = json.loads(set.def_topics)
        timeSE = timeStamp

        i=0
        for id in namesDict.keys():
            for top in namesDict[id].keys():
                if top in def_topics:
                    selTopics[top] = True
                    if i == 0:
                        topics[id] = {}
                        topics[id][top] = namesDict[id][top]
                        i = 1
                    else:
                        topics[id][top] = namesDict[id][top]
                else:
                    selTopics[top] = False
            i = 0

        sett = Set.query.filter_by(id=ids).first()

        for l in sett.log:
            log_ids.append(str(l.id))

        if topics == {}:
            for l in log_ids:
                topics[l] = {}

    else:
        log = Log.query.filter_by(id=ids).first()
        session_id = log.session_id
        def_topics = json.loads(log.def_topics)
        log_ids = [str(log.id)]

        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        (topList, fName) = getFileList(fileName, dirName)

        if "vehicle_gps_position_0" in topList:
            gpsAvail = log.defGPSCheck
            print("gps Available")

        (namesDict, timeStamp, timeUtc) = reader.readDataNames(log.id, dirName, fName, def_topics, gpsAvail)

        timeSE = timeStamp + timeUtc

        topics = {str(log.id): namesDict}

    return render_template("analyser2D.html", session=session_id, topics=topics, set=log_ids, type=type, id=ids, timeSE=timeSE, setIds=json.dumps(log_ids), gpsAvail=gpsAvail)

@app.route('/saveTopics', methods = ['POST'])
def saveTopics():
    print("saveTopics")
    topics = request.get_json()

    if topics["type"] == "log":
        log = Log.query.filter_by(id=topics["id"]).first()
        log.def_topics = json.dumps(topics["checkTopics"])
        db.session.commit()
    else:
        set = Set.query.filter_by(id=topics["id"]).first()
        gpsSetting = set.defGPSCheck
        dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
        lg_ids = []
        for log in set.log:
            lg_ids.append(log.id)
        topic_list = topics["checkTopics"]
        if (len(lg_ids) == 0) or (len(topic_list) == 0):
            print("Nothing selected. No changes have been made.")
            return jsonify(url_for('analyser2D', type=topics["type"], id=topics["id"]))

        mergedData = readAndMergeData(lg_ids, topic_list, gpsSetting)
        plugin = Plugins()
        plugin.addToMultipleLogs(mergedData, dirName, lg_ids)
        set.def_topics = json.dumps(topic_list)
        db.session.commit()

    resp = jsonify(url_for('analyser2D', type=topics["type"], id=topics["id"]))
    return resp

from analyser.Plotly import Plotly
import pandas as pd
@app.route('/postmethod', methods = ['GET','POST'])
def get_post_javascript_data():
    print("getPost")
    selections = request.get_json()
    reader = DataReader()
    ids = dict(selections["set_id"])
    xAxTime = selections["xAxTime"]

    if ids["type"] == "log":
        log = Log.query.filter_by(id=ids["id"]).first()
        if log is None:
            return jsonify({'error': 'Selected log doesnt exist anymore...'})
        log.defGPSCheck = 1 if xAxTime else 2
        db.session.commit()
        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        def_topics = json.loads(log.def_topics)

        data = reader.readDataFromDir(log.id, dirName, fileName, def_topics, xAxTime)

    else:
        sett = Set.query.filter_by(id=ids["id"]).first()
        if sett is None:
            return jsonify({'error': 'Selected set doesnt exist anymore...'})
        dirName = os.path.join(app.root_path, 'static', 'user_data', sett.dir_name)
        filename = dirName + '/' + 'merged.csv'
        data = pd.read_csv(filename)

    if data.empty:
        return jsonify({'error': 'Selected data set is empty. Try readjusting the filters...'})
    elif (selections["left"] == []) and (selections["right"] == []):
        return jsonify({'error': 'No parameters were selected. Add at least one parameter to the table...'})

    #FILTER
    filteredData = reader.selectedFilter(selections["filters"], data)

    axRg = selections["axisRange"]

    curr_project = current_user.get_id()
    setting = Settings.query.filter_by(project_id=curr_project).first()
    theme = "light" if setting.color_theme == "light" else "dark"

    plotly = Plotly()
    htmlFile = plotly.draw2D(filteredData, selections["left"], selections["right"], [axRg["left"][0],axRg["left"][1],axRg["right"][0],axRg["right"][1]], theme)
    resp = jsonify({'success':htmlFile, 'error': 'false'})
    return resp

@app.route('/chart3D', methods=['POST'])
def chart3D():
    print("chart3D")
    selections = request.get_json()
    reader = DataReader()
    print(selections)
    ids = dict(selections["set_id"])
    xAxTime = selections["xAxTime"]


    if ids["type"] == "log":
        log = Log.query.filter_by(id=ids["id"]).first()
        fileName = log.file_name
        log.defGPSCheck = 1 if xAxTime else 2
        db.session.commit()
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        def_topics = json.loads(log.def_topics)

        data = reader.readDataFromDir(log.id, dirName, fileName, def_topics, xAxTime)

    else:
        set = Set.query.filter_by(id=ids["id"]).first()
        dirName = os.path.join(app.root_path, 'static', 'user_data', set.dir_name)
        filename = dirName + '/' + 'merged.csv'
        data = pd.read_csv(filename)

    # Data FILTER
    filteredData = reader.selectedFilter(selections["filters"], data)

    # Time FILTER
    timeStamp = list(pd.to_datetime(filteredData['timestamp']).dt.round('ms').dt.strftime('%H:%M:%S.%f'))
    for t in range(len(timeStamp)):
        timeStamp[t] = str(timeStamp[t])[:-4]
    filteredData['timestamp'] = timeStamp
    # Select observations between two datetimes
    filteredData = filteredData[filteredData['timestamp'].between('{}.00'.format(selections["timeSEList"][0]), '{}.00'.format(selections["timeSEList"][1]))]

    dataLen = len(filteredData)
    if dataLen == 0:
        return jsonify({'error': 'Selected data set is empty. Try readjusting the filters...'})
    elif (selections["X"] == []) or (selections["Y"] == []) or (selections["Z"] == []) or ('set__-____-__data' in selections["X"]) or ('set__-____-__data' in selections["Y"]) or ('set__-____-__data' in selections["Z"]):
        return jsonify({'error': 'At least one parameter is not selected. Make sure, that all 3 axes have a value in the table.'})

    curr_project = current_user.get_id()
    setting = Settings.query.filter_by(project_id=curr_project).first()
    theme = "light" if setting.color_theme == "light" else "dark"

    legendNames = []
    for sel in range(len(selections["X"])):
        nameID = selections["X"][sel].split("__-__")[0]
        log = Log.query.filter_by(id=nameID).first()
        legendNames.append(log.title)

    plotly = Plotly()
    if selections["action"] == "Chart":
        htmlFile = plotly.draw3D(filteredData, selections["X"], selections["Y"], selections["Z"], selections["Color"], theme, legendNames)
    elif selections["action"] == "Sim":
        htmlFile = plotly.X2drawWithSliderReducedSteps(filteredData, selections["X"], selections["Y"], selections["Z"], selections["tail"], theme)

    resp = jsonify({'success':htmlFile, 'error': 'false'})
    return resp

import fnmatch
def getFileList(fileName, dirName):
    listOfCSVs = []
    fName = fileName.split('.')[0]
    fLen = len(fName) + 1
    for file in os.listdir(dirName):
        if fnmatch.fnmatch(file, '*.csv'):
            name = file.split('.')[0]
            listOfCSVs.append(name[fLen:])
    return (listOfCSVs, fName)


@app.route('/project/<session_id>', methods=["GET","POST"])
def session(session_id):
    print("session")
    curr_project = current_user.get_id()
    curr_session = Session.query.filter_by(id=session_id).first()
    curr_logs = Log.query.filter_by(session_id=session_id).all()
    curr_sets = Set.query.filter_by(session_id=session_id).all()
    sessions = Session.query.filter_by(project_id=curr_project).all()
    curr_tasks = list(reversed(Task.query.filter_by(session_id=session_id).all()))

    if request.method == 'POST':
        tk = Task(title=str(request.form['task']),
                  result='',
                  session_id=int(session_id))
        db.session.add(tk)
        db.session.commit()
        return redirect(url_for('session', session_id=session_id))

    return render_template("body.html", test_sessions=sessions,
                           sel_session=curr_session, logs=curr_logs,
                            tasks=curr_tasks, sets=curr_sets)

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    file_name, _ = os.path.splitext(form_file.filename)
    print("importing {}...".format(file_name))
    log_path = os.path.join(app.root_path, 'static', 'user_data', random_hex)
    while os.path.isdir(log_path):
        random_hex = secrets.token_hex(8)
        log_path = os.path.join(app.root_path, 'static', 'user_data', random_hex)
    os.mkdir(log_path)
    file_path = os.path.join(log_path, form_file.filename)
    form_file.save(file_path)

    converter = UlogConverter()
    converter.ulogToCSV(log_path, file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")

    return (random_hex, file_name)

def createSetDir():
    random_hex = secrets.token_hex(8)
    set_path = os.path.join(app.root_path, 'static/user_data', random_hex)
    while os.path.isdir(set_path):
        random_hex = secrets.token_hex(8)
        set_path = os.path.join(app.root_path, 'static/user_data', random_hex)
    os.mkdir(set_path)
    print("Directory created at {}".format(random_hex))
    return random_hex

def readAndMergeData(log_id_list, def_topics, syncOnGPS):
    reader = DataReader()
    allDataSet = []
    minTime = []
    maxTime = []
    lenOfData = []


    for lg in log_id_list:
        log = Log.query.filter_by(id=lg).first()
        fileName = log.file_name
        dirName = os.path.join(app.root_path, 'static', 'user_data', log.dir_name)
        (topList, fName) = getFileList(fileName, dirName)  # returns list of topic-names and filename (without .csv)
        lst = [x for x in def_topics if x in topList]
        dirData = reader.readDataFromDir(log.id, dirName, fName, lst, syncOnGPS)
        allDataSet.append(dirData)

        minTime.append(dirData['timestamp'].iloc[0])
        maxTime.append(dirData['timestamp'].iloc[-1])
        lenOfData.append(len(dirData))


    mergedData = allDataSet[0]

    #find the smallest time step in first dataset
    l1 = mergedData["timestamp"][1:].reset_index()
    l2 = mergedData["timestamp"][:-1].reset_index()
    steps = l1 - l2
    steps = steps.sort_values(by=["timestamp"])
    minStep = steps["timestamp"][int(len(steps)/100)]

    miTime = min(minTime)
    maTime = max(maxTime)

    dfTime = pd.DataFrame(pd.date_range(start=miTime, end=maTime, freq=minStep),columns=["timestamp"])
    mergedData = pd.merge_asof(left=dfTime, right=mergedData, on='timestamp', direction='nearest',
                  tolerance=pd.Timedelta('500ms'))

    for i in range(len(allDataSet) - 1):
        mergedData = pd.merge_asof(left=mergedData, right=allDataSet[i + 1], on='timestamp', direction='nearest',
                                   tolerance=pd.Timedelta('500ms'))

    print("Set data has been merged")
    print(f"Set Timestamp Range: {mergedData['timestamp'].iloc[0]} - {mergedData['timestamp'].iloc[-1]}")

    return mergedData

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

from io import BytesIO
from datetime import datetime
@app.route('/analyserXBackup')
def analyserXBackup():
    print("exporting files...")
    dbPath = os.path.join(app.root_path, "site.db")
    userDataPath = os.path.join(app.root_path,"static", "user_data")
    shutil.copy2(dbPath,userDataPath)
    time.sleep(0.5)

    #zipf = shutil.make_archive("exp", "tar", userDataPath, app.root_path)
    # create a ZipFile object
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zipf:
        for root, dirs, files in os.walk(userDataPath):
            for file in files:
                zipPath = os.path.relpath(root, userDataPath)
                zipf.write(os.path.join(root,file), os.path.join(zipPath, file))
    memory_file.seek(0)

    dbNewPath = os.path.join(userDataPath, "site.db")
    if os.path.exists(dbNewPath):
        os.remove(dbNewPath)
    else:
        print("The site.db in user_data not found...")

    print("export completed")

    dt_string = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

    return send_file(memory_file, attachment_filename = f"AnalyserX_Backup_{dt_string}.zip", as_attachment = True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['zip'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import zipfile
@app.route('/importData', methods=["GET","POST"])
def importData():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print("No file part in request")
            return render_template("import.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("No file selected...")
            flash("No file selected...", "warning")
            return render_template("import.html")
        if file and allowed_file(file.filename):
            print("Importing data...")
            zip_path = os.path.join(app.root_path, "import.zip")
            file.save(zip_path)
            zip_ref = zipfile.ZipFile(zip_path, 'r')
            temp_dir = os.path.join(app.root_path, "static", "temp")
            os.mkdir(temp_dir)
            zip_ref.extractall(temp_dir)
            zip_ref.close()

            shutil.move(os.path.join(temp_dir,"site.db"),os.path.join(app.root_path, "site.db"))
            user_d_path = os.path.join(app.root_path, "static", "user_data")
            remPath = os.path.join(app.root_path, "static", "oldData")
            os.rename(user_d_path, remPath)
            os.rename(temp_dir, user_d_path)
            shutil.rmtree(remPath)
            os.remove(zip_path)
            print("Data import completed")
            flash("Data import completed", "success")
            return redirect(url_for('home'))

    return render_template("import.html")