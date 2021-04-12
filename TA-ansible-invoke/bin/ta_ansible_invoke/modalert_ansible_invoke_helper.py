
# encoding = utf-8

# define a class to encapsulate Job template info
class JobTemplate():
    def __init__(self,id,name,launch_url):
        self.id=id
        self.name=name
        self.launch_url=launch_url


class Credential():
    def __init__(self,id,name):
        self.id=id
        self.name=name

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example gets account information
    user_account = helper.get_user_credential("<account_name>")

    # The following example gets the alert action parameters and prints them to the log
    request_id = helper.get_param("request_id")
    helper.log_info("request_id={}".format(request_id))

    technique_id = helper.get_param("technique_id")
    helper.log_info("technique_id={}".format(technique_id))

    technique_test_numbers = helper.get_param("technique_test_numbers")
    helper.log_info("technique_test_numbers={}".format(technique_test_numbers))

    ansible_awx_url = helper.get_param("ansible_awx_url")
    helper.log_info("ansible_awx_url={}".format(ansible_awx_url))

    ansible_awx_user = helper.get_param("ansible_awx_user")
    helper.log_info("ansible_awx_user={}".format(ansible_awx_user))

    ansible_awx_template = helper.get_param("ansible_awx_template")
    helper.log_info("ansible_awx_template={}".format(ansible_awx_template))

    ansible_awx_target = helper.get_param("ansible_awx_target")
    helper.log_info("ansible_awx_target={}".format(ansible_awx_target))

    ansible_awx_credentials = helper.get_param("ansible_awx_credentials")
    helper.log_info("ansible_awx_credentials={}".format(ansible_awx_credentials))

    splunk_hec_url = helper.get_param("splunk_hec_url")
    helper.log_info("splunk_hec_url={}".format(splunk_hec_url))

    splunk_hec_user = helper.get_param("splunk_hec_user")
    helper.log_info("splunk_hec_user={}".format(splunk_hec_user))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    
    import requests
    import json, time
    
    VERIFY_SSL_CERTIFICATE=False

    usehec = False
    account = helper.get_user_credential(helper.get_param("ansible_awx_user"))
    hec_account = None
    
    try:
        hec_account = helper.get_user_credential(helper.get_param("splunk_hec_user"))
        usehec = True
    except:
        helper.log_warn("Unable to locate HEC user - this can be safely ignored when HEC is not used to send Atomic summary to Splunk.")
        
    
    request_id = helper.get_param("request_id")
    helper.log_info("request_id={}".format(request_id))
    technique_id = helper.get_param("technique_id")
    helper.log_info("technique_id={}".format(technique_id))
    technique_test_numbers = helper.get_param("technique_test_numbers")
    helper.log_info("technique_test_numbers={}".format(technique_test_numbers))
    
    awx_url = helper.get_param("ansible_awx_url")
    helper.log_info("awx_url={}".format(awx_url))
    awx_template = helper.get_param("ansible_awx_template")
    helper.log_info("awx_template={}".format(awx_template))
    awx_target = helper.get_param("ansible_awx_target")
    helper.log_info("target={}".format(awx_target))
    awx_credentials = helper.get_param("ansible_awx_credentials")
    helper.log_info("awx_credentials={}".format(awx_credentials))
    splunk_hec_url = helper.get_param("splunk_hec_url")
    helper.log_info("splunk_hec_url={}".format(splunk_hec_url))
    
    
    AWX_HOST=awx_url
    AWX_USER=account['username']
    AWX_PASS=account['password']
    AWX_JOB_TEMPLATES_API = '{0}/api/v2/job_templates'.format(AWX_HOST)
    AWX_CREDENTIALS_API = '{0}/api/v2/credentials'.format(AWX_HOST)
    AWX_OAUTH2_TOKEN = None

    # check for token user - indicates we should use token auth
    if AWX_USER!="token":
        response = requests.post('{0}/api/v2/tokens/'.format(AWX_HOST), verify=VERIFY_SSL_CERTIFICATE, auth=(AWX_USER, AWX_PASS))
        AWX_OAUTH2_TOKEN = response.json()['token']
    else:
        AWX_OAUTH2_TOKEN = AWX_PASS
        
    AWX_OAUTH2_TOKEN_URL = '{0}{1}'.format(AWX_HOST,response.json()['url'])
    
    headers = {"User-agent": "splunk-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(AWX_OAUTH2_TOKEN)}
    job_template = awx_template
    job_credential = 'lab-windows-local'
    job_limit = awx_target
    
    splunk_hec_token = None
    
    if hec_account != None:
        splunk_hec_token = hec_account['password']
    
    
    helper.log_info("Starting...")
    
    # get the job template id
    response = requests.get(AWX_JOB_TEMPLATES_API, verify=VERIFY_SSL_CERTIFICATE, headers=headers)
    for job in response.json()['results']:
        jt = JobTemplate(job['id'], job['name'], AWX_HOST + job['related']['launch'])
    
        if(jt.name == job_template):
            helper.log_info("Job template {} located.".format(jt.name))
            break
    
    
    # get the credentials
    if(job_credential!=None and job_credential!=""):
        response = requests.get(AWX_CREDENTIALS_API, verify=VERIFY_SSL_CERTIFICATE, headers=headers)
        for cred in response.json()['results']:
            cr = Credential(cred['id'], cred['name'])
        
            if(cr.name == job_credential):
                helper.log_info("Credential {} located.".format(cr.name))
                break
    
        # launch template T1053 => T1218.010
        response = requests.post(jt.launch_url, verify=VERIFY_SSL_CERTIFICATE, headers=headers, data=json.dumps({'limit':job_limit,'credentials':[cr.id], 'extra_vars': { "technique_id": technique_id, "technique_test_numbers": technique_test_numbers, "send_results_to_hec": usehec, "splunk_hec_url": splunk_hec_url, "splunk_hec_token": splunk_hec_token , "request_id": request_id }}))
    else:
        response = requests.post(jt.launch_url, verify=VERIFY_SSL_CERTIFICATE, headers=headers, data=json.dumps({'limit':job_limit, 'extra_vars': { "technique_id": technique_id, "technique_test_numbers": technique_test_numbers, "send_results_to_hec": usehec, "splunk_hec_url": splunk_hec_url, "splunk_hec_token": splunk_hec_token , "request_id": request_id }}))

    
    if(response.status_code == 201):

        job_status_url = AWX_HOST + response.json()['url']
    
        helper.log_info("Job launched successfully.")
        helper.log_info("Job URL = {}".format(job_status_url))
    
        helper.log_info("Job id = {}".format(response.json()['id']))
        helper.log_info("Status = {}".format(
            response.json()['status']))
        helper.log_info(
            "Waiting for job to complete (timeout = 15mins).")
        timeout = time.time() + 60*15
    
        while(True):
            time.sleep(2)
    
            job_response = requests.get(
                job_status_url, verify=VERIFY_SSL_CERTIFICATE, headers=headers)
            if(job_response.json()['status'] == "new"):
                helper.log_info("Job status = new.")
            if(job_response.json()['status'] == "pending"):
                helper.log_info("Job status = pending.")
            if(job_response.json()['status'] == "waiting"):
                helper.log_info("Job status = waiting.")
            if(job_response.json()['status'] == "running"):
                helper.log_info("Job status = running.")
            if(job_response.json()['status'] == "successful"):
                helper.log_info("Job status = successful.")
                break
            if(job_response.json()['status'] == "failed"):
                helper.log_error("Job status = failed.")
                break
            if(job_response.json()['status'] == "error"):
                helper.log_error("Job status = error.")
                break
            if(job_response.json()['status'] == "canceled"):
                helper.log_error("Job status = canceled.")
                break
            if(job_response.json()['status'] == "never updated"):
                helper.log_error("Job status = never updated.")
    
            # timeout of 15m break loop
            if time.time() > timeout:
                helper.log_warn("Timeout after 15mins.")
                break
    
        helper.log_info("Fetching Job stdout")
        job_stdout_response = requests.get(AWX_HOST + response.json()['related']['stdout'] + "?format=json", verify=VERIFY_SSL_CERTIFICATE, headers=headers)
    
        helper.log_info(job_stdout_response.json()['content'])
    else:
        helper.log_error(response.json())
    
    response = requests.delete(AWX_OAUTH2_TOKEN_URL, verify=VERIFY_SSL_CERTIFICATE, auth=(AWX_USER, AWX_PASS))
    helper.log_info("Done.")

    # TODO: Implement your alert action logic here
    return 0
