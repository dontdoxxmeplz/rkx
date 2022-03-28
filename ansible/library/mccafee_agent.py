#!/usr/bin/env python3

import pathlib, subprocess
from ansible.module_utils.basic import AnsibleModule

MCCAFEE_MANAGING_SCRIPTS = ([
    '/opt/McAfee/ens/tp/init/mfetpd-control.sh',
    '/opt/McAfee/ens/esp/init/mfeespd-control.sh',
    '/opt/isec/ens/threatprevention/bin/isectpdControl.sh',
    '/opt/isec/ens/esp/bin/isecespdControl.sh'
])

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mccafee_agent

short_description: MCcafee Antivirus Linux agent manager.

version_added: "1.0"

description:
    - Use this module to change MCcafee Linux agent state on a local or remote systems.
    - https://kc.mcafee.com/corporate/index?page=content&id=KB88223

options:
    state:
        description:
            - Specify the desired state of the system's Mccafee agent.
        required: false
        default: 'start'
        type: str
        choices: ['started', 'stopped']
    enabled:
        description:
            - Specify Mccafee should be enabled or not.
        required: false
        default: None
        type: bool
'''

EXAMPLES = '''
- name: Start and enable MCcafee linux agent
  mccafee_agent:
    state: started
    enabled: true
'''

RETURN = '''
changed:
    description: Whether the module performed an action or not
    type: bool
message:
    description: The output message that the sample module generates
    type: str
'''

def executeProcess(cmd=""):
    try:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    except Exception as err:
        return err

def run_module():
    # module arguments
    module_args = dict(
        state=dict(type='str', required=False, default="start"),
        enabled=dict(type='bool', required=False, default=None)
    )

    # results dictionary
    result = dict(
        changed=False,
        message='The MCcafee Agent is not installed on the system.'
    )

    # create ansible module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # set local variables
    mccafee_state = 'start' if module.params['state'] == 'started' else 'stop'
    mccafee_enabled = 'enable' if module.params['enabled'] == True else 'disable'

    for script in MCCAFEE_MANAGING_SCRIPTS:
        file = pathlib.Path(script)
        if file.exists():
            res_state = executeProcess(script + " " + mccafee_state)
            res_enable = executeProcess(script + " " + mccafee_enabled) if module.params['enabled'] != None else 'NA'
            result['changed'] = True
            result['message'] += "{}".format(res_state) + "{}".format(res_enable)

    # exit with results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()