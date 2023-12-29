from flask import Flask
from flask import render_template
from ec2_describe import ec2_describe
app = Flask(__name__)










@app.route('/')
def hello_world():
    instance_list = ec2_describe()
    return render_template("index.html", template_instance_list=instance_list )