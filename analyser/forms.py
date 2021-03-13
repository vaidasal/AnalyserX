from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError
from analyser.models import Project
from wtforms.widgets import TextArea


class NewProjectForm(FlaskForm):
    project_name = StringField('Title',
                              validators=[DataRequired()])
    project_description = StringField('Description', widget=TextArea())
    company = StringField('Company')
    engineer = StringField('Engineer')
    submit = SubmitField('Create')

    def validate_project_name(self, project_name):
        project = Project.query.filter_by(title=project_name.data).first()
        if project:
            raise ValidationError('This project name is taken.')

class SelectProjectForm(FlaskForm):
    project_name = SelectField(label='Project Name', choices=[])
    submit = SubmitField('Enter')

class AddSessionForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=1)]
                        )
    notes = StringField(label='Notes', widget=TextArea())
    add = SubmitField('Create')

class AddLogForm(FlaskForm):
    title = StringField('Title',
                        #validators=[DataRequired(), Length(min=2, max=20)]
                        )
    notes = StringField(label='Notes', widget=TextArea())
    log_file = MultipleFileField('Add Log', validators=[FileAllowed(['ulg'])])
    add_file = SubmitField('Add')
