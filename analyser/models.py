from analyser import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_project(project_id):
    return Project.query.get(int(project_id))

class Project(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=True)
    company = db.Column(db.String(), nullable=True)
    engineer = db.Column(db.String(), nullable=True)
    session = db.relationship('Session', backref='author', lazy=True)
    settings = db.relationship('Settings', backref='author', lazy=True)

    def __repr__(self):
        return f"Project('{self.title}','{self.description}')"

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String(), nullable=True)
    log = db.relationship('Log', backref='author', lazy=True)
    task = db.relationship('Task', backref='author', lazy=True)
    set = db.relationship('Set', backref='author', lazy=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"Session('{self.title}')"

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String(), nullable=True)
    def_topics = db.Column(db.String())
    file_name = db.Column(db.String())
    topic = db.relationship('Topics', backref='author', lazy=True)
    dir_name = db.Column(db.String())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    #set_id = db.Column(db.Integer, db.ForeignKey('set.id'), nullable=True)

    def __repr__(self):
        return f"{self.id}"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    result = db.Column(db.String(), nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}')"

association_set_log = db.Table('association', db.Model.metadata,
                            db.Column('Set', db.Integer, db.ForeignKey('set.id')),
                            db.Column('Log', db.Integer, db.ForeignKey('log.id'))
                            )

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String(), nullable=True)
    dir_name = db.Column(db.String())
    def_topics = db.Column(db.String())
    log = db.relationship('Log', backref='logAuthor', secondary=association_set_log)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    def __repr__(self):
        return f"Set('{self.title}')"

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    topics = db.Column(db.String())
    color_theme = db.Column(db.String(), default="dark")

    def __repr__(self):
        return f"Settings('{self.id}')"

class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    topic_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Topics('{self.topic_name}')"