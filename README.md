# TA-ansible-invoke

Ansible AWX Atomic Red Red Execution Add-on for Splunk

Example execution:

```bash
| sendalert ansible_invoke \
    param.request_id=<unique id> \
    param.technique_id="<technique id (e.g. T1053.005)>" \
    param.technique_test_numbers="<comma separated test numbers. use 0 for all>" \
    param.ansible_awx_user="<splunk global account username configured in the TA. used to authenticate to AWX. to use a token ensure the username is 'token'>" \
    param.ansible_awx_template="<the template to use for execution>" \
    param.ansible_awx_target="<the target host to run against. this is the 'limit' arguement to the template. wildcards can be used>" \
    param.ansible_awx_url="<ansible server url (e.g. https://ansible.mydomain.com)>" \
    param.splunk_hec_url="<splunk hec url. passed to the powershell script in the playbook to allow hec push>" \
    param.splunk_hec_user="<splunk hec username global account username lookup for hec token>"
```
