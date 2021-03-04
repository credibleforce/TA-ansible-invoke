
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_ansible_invoke_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_ansible_invoke_helper

class AlertActionWorkeransible_invoke(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkeransible_invoke, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_param("global_account_name"):
            self.log_error('global_account_name is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("awx_url"):
            self.log_error('awx_url is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("request_id"):
            self.log_error('request_id is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("technique_id"):
            self.log_error('technique_id is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("technique_test_numbers"):
            self.log_error('technique_test_numbers is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("target"):
            self.log_error('target is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_ansible_invoke_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(str(ae)))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e:
                self.log_error(msg.format(str(e)))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkeransible_invoke("TA-ansible-invoke", "ansible_invoke").run(sys.argv)
    sys.exit(exitcode)
