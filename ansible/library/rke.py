#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: rke

short_description: Kubernetes RKE

version_added: "1.0"

description:
    - Kubernetes RKE distribution Ansible module

dependencies:
    - RKE binary
    - 

options:
    state:
        description:
            - Specify the desired state of the module.
        required: true
        type: str
        choices: ['present', 'absent', 'latest']
'''

EXAMPLES = '''
- name: Start and enable MCcafee linux agent
  module_name:
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

def run_module():
    # module arguments
    module_args = dict(
        state=dict(type='str', required=False, default="start"),
        enabled=dict(type='bool', required=False, default=None)
    )

    # results dictionary
    result = dict(
        changed=False,
        message='Default message.'
    )

    # create ansible module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result['changed'] = True
    result['message'] = "Returned message"

    # exit with results
    try:
        module.exit_json(**result)
    except Exception as err:
        result['message'] = 'Error message'
        module.fail_json(msg=result['message'])
        module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()