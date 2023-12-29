from flask import Flask
from flask import render_template
from ec2_describe import ec2_describe
import pprint
app = Flask(__name__)


@app.route('/')
def index():
    instance_list = ec2_describe()
    instance_ids = []
    for instance in instance_list:
        instance_ids.append(instance['InstanceId'])
    return render_template("index.html", template_instance_list=instance_list )

@app.route('/instance/<instance_id>')
def instance_details(instance_id):
    instance_list = ec2_describe()
    # Creating a list based on the url re-direct instance_id so each detailed page breakdown will be unique to the instanceID that was clicked
    instance_detailed_dict = {}
    for instance in instance_list:
        if instance['InstanceId'] == instance_id:
            instance_detailed_dict.update(instance)
            break
    print(instance_detailed_dict)
            

    return render_template("instance.html", template_instance_list=instance_list, template_instance_details=instance_detailed_dict)


