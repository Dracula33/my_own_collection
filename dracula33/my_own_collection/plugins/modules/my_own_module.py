#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my test module from homework.

version_added: "1.0.0"

description: It can create files

options:
    path:
        description: This is the path where file will be created
        required: true
        type: str
    content:
        description: Content of creating file. If it is not set, it will be an empty string
        required: false
		default: ''
        type: str
		
author:
    - Igor S
'''

EXAMPLES = r'''
# Create file with 'Hello World' content
- name: Create file with Hello World!
  dracula33.my_collection.my_own_module:
    path: ./file.txt
    content: Hello World!
'''

RETURN = r'''
result_code:
    description: Return code of operation's result. 0 - success, 1 - error
    type: int
    returned: always
    sample: 1
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # input values
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='')
    )

    # return value
    result = dict(
        changed=False,
        result_code=0
    )

    # no check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    #проверка на наличие файла с таким именем и содержимым
    current_content = ''
    try:
        with open(module.params['path'], 'r') as file:
            current_content = file.read()
    except FileNotFoundError:
        pass
    except Exception as err:
        result['result_code'] = 1
        module.fail_json(msg=type(err).__name__ + str(err), **result)

    if current_content == module.params['content']:
        module.exit_json(**result)

    try:
        with open(module.params['path'], 'w') as file:
            file.write(module.params['content'])
    except Exception:
        result['result_code'] = 2
        module.fail_json(msg='Error while creating file', **result)

    result['changed'] = True
    # success
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
