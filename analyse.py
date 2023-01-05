import openshift as oc
from datetime import datetime

namespace="demo"

print('{:20}   {:10}   {:10}   {}'.format("Name", "Created", "Started", "Latency"))

with oc.project(oc.get_project_name()), oc.timeout(10*60):
    for pr_obj in oc.selector('pipelineruns').objects():
        # print('Analyzing PipelineRun: {}'.format(pr_obj.name()))
        pr_model = pr_obj.model
        timestamp_format='%Y-%m-%dT%H:%M:%SZ'
        pr_creation_time = datetime.strptime(pr_model.metadata.creationTimestamp, timestamp_format)
        pr_start_time = datetime.strptime(pr_model.status.startTime, timestamp_format)
        latency = pr_start_time - pr_creation_time

        print('{:20}   {:10}   {:10}   {} seconds'.format(pr_obj.name(), 
                pr_creation_time.strftime("%H:%M:%S"), 
                pr_start_time.strftime("%H:%M:%S"), 
                latency.total_seconds()))

