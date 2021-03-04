# TA-ansible-invoke

Ansible AWX Atomic Red Red Execution Add-on for Splunk

Example execution:

```bash
| sendalert ansible_invoke \
    param.request_id=<unique id> \
    param.technique_id="<technique id (e.g. T1053.005)>" \
    param.technique_test_numbers="<comma separated test numbers. use 0 for all>" \
    param.global_account_name="<splunk global account username configured in the TA. used to authenticate to AWX. to use a token ensure the username is 'token'>" \
    param.target="<the target host to run against. this is the 'limi' arguement to the template. wildcards can be used>" \
    param.awx_url="<ansible server url (e.g. https://ansible.mydomain.com)>" \
    param.splunk_hec_url="<splunk hec url. not currently used>" \
    param.splunk_hec_username="<splunk hec username global account username lookup>"
```
