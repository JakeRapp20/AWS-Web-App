from flask import Flask, render_template, request, redirect, session, url_for
from ec2 import ec2_describe, backend_ec2_stop, backend_ec2_start
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import boto3
import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)



# FORMS to get AWS Creds and REGION
class SecretAccessKeyForm(FlaskForm):
    access_key = StringField('What is your Access Key?', validators=[DataRequired()])
    secret_access_key = StringField('What is your Secret Access Key?', validators=[DataRequired()])
    region = StringField('What AWS Region?', validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route('/', methods=['GET', 'POST'])
def index():

    # initialize aws creds and region vars then saves form data to session 
    secret_access_key = None
    access_key = None
    region = None
    access_key_form = SecretAccessKeyForm()
    secret_access_key_form = SecretAccessKeyForm()
    region_form = SecretAccessKeyForm()
    if access_key_form.validate_on_submit() and secret_access_key_form.validate_on_submit() and region_form.validate_on_submit():
        session['access_key'] = access_key_form.access_key.data
        session['secret_access_key'] = secret_access_key_form.secret_access_key.data
        session['region'] = region_form.region.data
        return redirect(url_for('index'))

    return render_template("index.html", 
                           template_access_key_form=access_key_form,
                           template_secret_access_key_form=secret_access_key_form, 
                           template_region_form=region_form,
                           template_secret_access_key=secret_access_key,
                           template_access_key=access_key,
                           template_region=region,
                           aws_access_key=session.get('access_key'),
                           aws_secret_access_key=session.get('secret_access_key'),
                           region=session.get('region')
             
                        )



@app.route('/ec2', methods=['GET', 'POST'])
def ec2_summary():
    instance_list = ec2_describe()
    instance_ids = []
    instances_to_stop_or_start = []
    status = ''
    form = None
    for instance in instance_list:
        instance_ids.append(instance['InstanceId'])
    # if request.method == 'POST':
    #     for instance in instance_list:
    #         if request.form[instance['InstanceId']] == 'Stop':
    #             instances_to_stop_or_start.append(instance['InstanceId'])
    #             ec2_stop(instances_to_stop_or_start)
    #             status = 'Stopping'
    #             return redirect(url_for('ec2_summary'))
    #         if request.form[instance['InstanceId']] == 'Start':
    #             instances_to_stop_or_start.append(instance['InstanceId'])
    #             ec2_start(instances_to_stop_or_start)
    #             status = 'Starting'
    #             return redirect(url_for('ec2_summary'))
    #         else:
    #             pass
    
    # elif request.method == 'GET':

    return render_template("ec2.html", template_instance_list=instance_list, template_session=session, aws_access_key=session.get('access_key'),
                           aws_secret_access_key=session.get('secret_access_key'), ec2_status=status)



@app.route('/instance/<instance_id>')
def instance_details(instance_id):
    instance_list = ec2_describe()
    # Creating a list based on the url re-direct instance_id so each detailed page breakdown will be unique to the instanceID that was clicked
    instance_detailed_dict = {}
    for instance in instance_list:
        if instance['InstanceId'] == instance_id:
            instance_detailed_dict.update(instance)
            break

    return render_template("instance.html", template_instance_list=instance_list, template_instance_details=instance_detailed_dict)

@app.route('/stop-instance/<instance_id>')
def ec2_stop(instance_id):

    backend_ec2_stop(instance_id)
    return redirect(url_for('ec2_summary'))



@app.route('/start-instance/<instance_id>')
def ec2_start(instance_id):
    print("It's working"
    )
    backend_ec2_start(instance_id)
    return redirect(url_for('ec2_summary'))

