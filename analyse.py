import openshift as oc, pandas as pd
from datetime import datetime

namespace="demo"

print('{:20}   {:10}   {:10}   {}'.format("Name", "Created", "Started", "Latency"))

pr_list={}

with oc.project(oc.get_project_name()), oc.timeout(10*60):
    for pr_obj in oc.selector('pipelineruns').objects():
        pr_model = pr_obj.model
        timestamp_format='%Y-%m-%dT%H:%M:%SZ'
        pr_creation_time = datetime.strptime(pr_model.metadata.creationTimestamp, timestamp_format)
        pr_start_time = datetime.strptime(pr_model.status.startTime, timestamp_format)
        latency = pr_start_time - pr_creation_time

        pr_list[pr_obj.name()] = {
            'created': pr_creation_time,
            'started': pr_start_time,
            'latency': latency
        }

        print('{:20}   {:10}   {:10}   {} seconds'.format(pr_obj.name(), 
                pr_creation_time.strftime("%H:%M:%S"), 
                pr_start_time.strftime("%H:%M:%S"), 
                latency.total_seconds()))


pr_df = pd.DataFrame.from_dict(data=pr_list, orient='index')
print(pr_df)

excel_writer = pd.ExcelWriter('tmp/pr-list-' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.xlsx')
pr_df.to_excel(excel_writer)
excel_writer.save()


