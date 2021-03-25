Role Name
=========

- role_deploy_webhook_proxy

      This role deploys proxy as a service on the target server

Role Variables
--------------

- webhook_proxy_directory

Dependencies
------------

- NA

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      roles:
         - role_deploy_webhook_proxy
      vars:
        webhook_proxy_directory: "/data/webhook/proxy"
        

Testing Platform
----------------

- Red Hat Enterprise Linux Server release 7.6 (Maipo)

Author Information
------------------

- Yasin Faizan S MD
