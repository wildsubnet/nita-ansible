#!/usr/bin/env python3
# ********************************************************
#
# Project: nita-ansible
#
# Copyright (c) Juniper Networks, Inc., 2025. All rights reserved.
#
# Notice and Disclaimer: This code is licensed to you under the Apache 2.0 License (the "License"). You may not use this code except in compliance with the License. This code is not an official Juniper product. You can obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.html
#
# SPDX-License-Identifier: Apache-2.0
#
# Third-Party Code: This code may depend on other components under separate copyright notice and license terms. Your use of the source code for those components is subject to the terms and conditions of the respective license as noted in the Third-Party source code file.
#
# ********************************************************

"""Utility functions for interacting with the AWX (Ansible Automation Platform) REST API.

This module provides helper functions for authenticating with an AWX server and
performing common CRUD operations on AWX resources, including inventories, hosts,
groups, organizations, projects, execution environments, and job templates.

Typical usage involves calling the ``add_*`` and ``get_*`` helpers in sequence
to bootstrap a fully configured AWX environment from structured data.

Module-level constants ``awx``, ``user``, and ``password`` supply default
connection parameters that can be overridden on a per-call basis.
"""

import requests
import sys
import json
import base64

user="awx"
password="Juniper!1"
credentials=f"{user}:{password}"
encodeded_credentials=base64.b64encode(credentials.encode()).decode()
awx="http://127.0.0.1:31768"

def get_awx (sub_url,awx=awx,user=user,password=password):
    """Send an authenticated GET request to the AWX API.

    Verifies server availability via the ``/api/login`` endpoint before issuing
    the actual request. Appends ``?format=json`` to the URL if not already
    present.

    Args:
        sub_url (str): The API sub-path to request (e.g. ``/api/v2/inventories``).
        awx (str): Base URL of the AWX server. Defaults to the module-level
            ``awx`` value.
        user (str): AWX username for basic authentication. Defaults to the
            module-level ``user`` value.
        password (str): AWX password for basic authentication. Defaults to the
            module-level ``password`` value.

    Returns:
        requests.Response: The HTTP response from the GET request.

    Raises:
        SystemExit: If the login check returns a non-200 status or a
            ``requests.exceptions.RequestException`` is raised.
    """
    fmt="?format=json"
    if fmt in sub_url:
       fmt=""
    header={'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
      response=requests.get(awx+"/api/login",auth=(user,password))
      if response.status_code != 200:
        print(f"Server unavailable: {response.status_code} {response.text}")
        sys.exit()
      print ("get: "+awx+sub_url+fmt)
      return requests.get(awx+sub_url+fmt,auth=(user,password),headers=header)
    except requests.exceptions.RequestException as e:
      print(f"Server unavailable: {e}")
      sys.exit()
    #response=requests.get(awx+"/api/login",auth=(user,password))
    #if response.status_code != 200:
    #  print(f"Server unavailable: {response.status_code} {response.text}")
    #  sys.exit()
    #print ("get: "+awx+sub_url+fmt)
    #return requests.get(awx+sub_url+fmt,auth=(user,password),headers=header)

def patch_awx (sub_url, jsonData,awx=awx,user=user,password=password):
    """Send an authenticated PATCH request to the AWX API.

    Verifies server availability via the ``/api/login`` endpoint before issuing
    the PATCH request. Appends ``?format=json`` to the URL if not already
    present.

    Args:
        sub_url (str): The API sub-path to patch
            (e.g. ``/api/v2/hosts/1/variable_data/``).
        jsonData (str): JSON-encoded string with the data to send in the request
            body.
        awx (str): Base URL of the AWX server. Defaults to the module-level
            ``awx`` value.
        user (str): AWX username for basic authentication. Defaults to the
            module-level ``user`` value.
        password (str): AWX password for basic authentication. Defaults to the
            module-level ``password`` value.

    Returns:
        requests.Response or None: The HTTP response from the PATCH request, or
        ``None`` if an HTTP 400 error is caught.

    Raises:
        SystemExit: If a ``requests.exceptions.RequestException`` is raised.
    """
    fmt="?format=json"
    if fmt in sub_url:
       fmt=""
    header={'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
      response=requests.get(awx+"/api/login",auth=(user,password))
      #if response.status_code != 200:
      #  print(f"Server unavailable: {response.status_code} {response.text}")
      #  sys.exit()
      #print ("patch: "+awx+sub_url)
      return requests.patch(awx+sub_url,data=jsonData,auth=(user,password),headers=header)
    except requests.exceptions.HTTPError as http_err:
      if response.status_code == 400:
        print("400 Bad Request: {http_err}")
    except requests.exceptions.RequestException as e:
      print(f"Server unavailable: {e}")
      sys.exit()
    #response=requests.get(awx+"/api/login",auth=(user,password))
    #if response.status_code != 200:
    #  print(f"Server unavailable: {response.status_code} {response.text}")
    #  sys.exit()
    #print ("patch: "+awx+sub_url)
    #return requests.patch(awx+sub_url,data=dataDict,auth=(user,password),headers=header)
    
def post_awx (sub_url, jsonData,awx=awx,user=user,password=password):
    """Send an authenticated POST request to the AWX API.

    Verifies server availability via the ``/api/login`` endpoint before issuing
    the POST request. Calls ``raise_for_status()`` on the response so that HTTP
    error codes surface as exceptions.

    Args:
        sub_url (str): The API sub-path to post to
            (e.g. ``/api/v2/inventories/``).
        jsonData (str): JSON-encoded string with the data to send in the request
            body.
        awx (str): Base URL of the AWX server. Defaults to the module-level
            ``awx`` value.
        user (str): AWX username for basic authentication. Defaults to the
            module-level ``user`` value.
        password (str): AWX password for basic authentication. Defaults to the
            module-level ``password`` value.

    Returns:
        requests.Response or str: The HTTP response object on success, or the
        string ``"400 Bad Request"`` when the server returns a 400 status code.
    """
    fmt="?format=json"
    if fmt in sub_url:
       fmt=""
    header={'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
      response=requests.get(awx+"/api/login",auth=(user,password))
      #if response.status_code != 200:
      #  print(f"Server unavailable: {response.status_code} {response.text}")
      #  sys.exit()
      #print ("post: "+awx+sub_url)
      response=requests.post(awx+sub_url,data=jsonData,auth=(user,password),headers=header)
      response.raise_for_status()
      
      return response
    except requests.exceptions.HTTPError as err:
      if response.status_code == 400:
        print(f"400 Bad Request: {err}")
        return "400 Bad Request"
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")


def get_inventory (inventory_name,awx=awx,user=user,password=password):
  """Retrieve an AWX inventory by name.

  Args:
      inventory_name (str): The name of the inventory to look up.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 4-tuple ``(dict, int, str, int)`` containing:
          - The matched inventory dict, or the full results dict if not found.
          - The inventory ID (``0`` if not found).
          - The inventory description (empty string if not found).
          - The organization ID (``0`` if not found).
  """
  inventories=get_awx("/api/v2/inventories",awx,user,password)
  dictInventory=json.loads(inventories.text)
  for dict in dictInventory['results']:
    if dict['name'] == inventory_name:
      return dict,dict['id'],dict['description'],dict['organization']  
  return dictInventory,0,"",0   

def get_inv_group (group_name,inventory_id,awx=awx,user=user,password=password):
  """Retrieve the ID of a named group within an AWX inventory.

  Args:
      group_name (str): The name of the group to look up.
      inventory_id (int): The ID of the inventory containing the group.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      int: The group ID if found, or ``0`` if no matching group exists.
  """
  groups = get_awx(f"/api/v2/inventories/{inventory_id}/groups/",awx,user,password)
  groupsInv = json.loads(groups.text)
  for group in groupsInv['results']:
    if group['name'] == group_name:
      return group['id']
  return 0

def get_host (host_name,inventory_id,awx=awx,user=user,password=password):
  """Retrieve a named host from an AWX inventory.

  Args:
      host_name (str): The name of the host to look up.
      inventory_id (int): The ID of the inventory to search.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(dict, int)`` containing:
          - The matched host dict, or the full results dict if not found.
          - The host ID (``0`` if not found).
  """
  hosts = get_awx(f"/api/v2/inventories/{inventory_id}/hosts/",awx,user,password)
  hosts_inv = json.loads(hosts.text)
  for host in hosts_inv['results']:
    if host['name'] == host_name:
      return host,host['id']
  return hosts_inv,0

def get_job_templates (orgid,awx=awx,user=user,password=password):
  """Retrieve all job templates belonging to an AWX organization.

  Args:
      orgid (int): The ID of the AWX organization.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      dict: The parsed JSON response containing job template data, including a
      ``results`` list of job template objects.
  """
  jobs=get_awx(f"/api/v2/organizations/{orgid}/job_templates",awx,user,password)
  job_templates=json.loads(jobs.text)
  return job_templates

def get_org (inventory_name,awx=awx,user=user,password=password):
  """Retrieve an AWX organization by name.

  Args:
      inventory_name (str): The name of the organization to look up.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(dict, int)`` containing:
          - The matched organization dict, or the last iterated dict if not
            found.
          - The organization ID (``0`` if not found).
  """
  org=get_awx("/api/v2/organizations",awx,user,password)
  org_dict=json.loads(org.text)
  for dict in org_dict['results']:
    if dict['name'] == inventory_name:
      return dict,dict['id']  
  return dict,0

def get_project (orgid,name,awx=awx,user=user,password=password):
  """Retrieve a named project within an AWX organization.

  Args:
      orgid (int): The ID of the organization to search within.
      name (str): The name of the project to look up.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(dict, int)`` containing:
          - The matched project dict, or the last iterated dict if not found.
          - The project ID (``0`` if not found).
  """
  projects=get_awx(f"/api/v2/organizations/{orgid}/projects",awx,user,password)
  project_dict=json.loads(projects.text)
  for dict in project_dict['results']:
    if dict['name'] == name:
      return dict,dict['id'],
  return dict,0

def get_ee(environment_name,awx=awx,user=user,password=password):
  """Retrieve the ID, description, and image of an AWX execution environment by name.

  Args:
      environment_name (str): The name of the execution environment to look up.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple or None: A 3-tuple ``(int, str, str)`` containing the execution
      environment's ID, description, and image URI if found; otherwise ``None``.
  """
  try:
    response = get_awx(f"/api/v2/execution_environments/",awx,user,password)

    if response.status_code == 200:
      # Parse the JSON response
      environments = response.json()["results"]
      for environment in environments:
        if environment["name"] == environment_name:
          return environment["id"],environment["description"],environment["image"]

    """
      #if the environment is not found in the first page, check subsequent pages
      while "next" in response.json():
        response = get_awx(response.json()["next"])
        environments = response.json()["results"]
        for environment in environments:
          if environment["name"] == environment_name:
            return environment["id"]
    """
    return None

  except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    return None

def add_ee (name, description, image,pull,awx=awx,user=user,password=password):
  """Create a new execution environment in AWX.

  If the POST request returns a 400 Bad Request (indicating the execution
  environment already exists), the existing environment's ID is fetched via
  ``get_ee``.

  Args:
      name (str): The name for the execution environment.
      description (str): A human-readable description.
      image (str): The container image URI for the execution environment.
      pull (str): The image pull policy
          (e.g. ``"always"``, ``"missing"``, ``"never"``).
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created or existing execution environment
            (``0`` on failure).
  """
  ee_id = 0
  ee_dict={}
  ee_dict["name"]=name
  ee_dict["description"]=description
  ee_dict["image"]=image
  ee_dict["pull"]=pull
  final_ee=json.dumps(ee_dict)
  response=post_awx(f"/api/v2/execution_environments/",final_ee,awx,user,password)
  if response != "400 Bad Request":
    if response.status_code == 201:
      ee_id=json.loads(response.text)['id']
  else:
    ee_id,ee_desc,ee_env=get_ee(name,awx,user,password)

  return response, ee_id

def add_host (inventory_id, host_data, var_data,awx=awx,user=user,password=password):
  """Add a host to an AWX inventory, including its variable data.

  If the POST request returns a 400 Bad Request (indicating the host already
  exists), the existing host's ID is fetched via ``get_host``. On a successful
  201 creation, a PATCH request is sent to set the host's variable data.

  Args:
      inventory_id (int): The ID of the inventory to add the host to.
      host_data (str): JSON-encoded string with host attributes (must include
          ``name``).
      var_data (str): JSON-encoded string with the host's variable data.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the last request issued.
          - The ID of the created or existing host (``0`` on failure).
  """
  #print(f">>>>Add Host Function: {inventory_id} {host_data}")
  host_id = 0
  response=post_awx(f"/api/v2/inventories/{inventory_id}/hosts/",host_data,awx,user,password)
  if response != "400 Bad Request":
    if response.status_code == 201:
      host_id=json.loads(response.text)['id']
      response=patch_awx(f"/api/v2/hosts/{host_id}/variable_data/",var_data,awx,user,password)
  else:
    #
    # get_host returns host struct and host_id...only need ID
    #
    response,host_id=get_host(json.loads(host_data)['name'],inventory_id,awx,user,password)
  return response, host_id

def add_host_to_group (host_id,group_id,awx=awx,user=user,password=password):
  """Associate an existing host with an AWX inventory group.

  Args:
      host_id (int): The ID of the host to add.
      group_id (int): The ID of the group to add the host to.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      requests.Response or str: The HTTP response from the POST request, or
      ``"400 Bad Request"`` if the association already exists.
  """
  host_dict={}
  host_dict['id']=host_id
  final_group=json.dumps(host_dict)
  response=post_awx(f"/api/v2/groups/{group_id}/hosts/",final_group,awx,user,password)
  return response

def add_child_to_group (child_id,group_id,awx=awx,user=user,password=password):
  """Associate a child group with a parent AWX inventory group.

  Args:
      child_id (int): The ID of the child group to nest.
      group_id (int): The ID of the parent group.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      requests.Response or str: The HTTP response from the POST request, or
      ``"400 Bad Request"`` if the relationship already exists.
  """
  child_dict={}
  child_dict['id']=child_id
  final_group=json.dumps(child_dict)
  response=post_awx(f"/api/v2/groups/{group_id}/children/",final_group,awx,user,password)
  return response

def add_inventory(orgid,invname,awx=awx,user=user,password=password):
  """Create a new inventory in an AWX organization.

  If the POST request returns a 400 Bad Request (indicating the inventory
  already exists), the existing inventory's ID is fetched via ``get_inventory``.

  Args:
      orgid (int): The ID of the organization that will own the inventory.
      invname (str): The name for the new inventory (also used as description).
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created or existing inventory (``0`` on failure).
  """
  inventory_id = 0
  inventory_dict={}
  inventory_dict['name']=invname

  inventory_dict['description']=invname
  inventory_dict['organization']=orgid
  final_inventory=json.dumps(inventory_dict)
  response=post_awx(f"/api/v2/inventories/",final_inventory,awx,user,password)
  if response != "400 Bad Request":
    if response.status_code == 201:
      inventory_id=json.loads(response.text)['id']
  else:
    inv,inventory_id,inv_desc,inv_org=get_inventory(invname,awx,user,password) 
  return response, inventory_id  

def add_inv_group(group,description,inv_id,group_variables,awx=awx,user=user,password=password):
  """Create a new group within an AWX inventory.

  If the POST request returns a 400 Bad Request (indicating the group already
  exists), the existing group's ID is fetched via ``get_inv_group``.

  Args:
      group (str): The name of the group to create.
      description (str): A human-readable description for the group.
      inv_id (int): The ID of the inventory to add the group to.
      group_variables (str): A JSON or YAML string of variables to assign to
          the group.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created or existing group (``0`` on failure).
  """
  group_id = 0
  group_dict={}
  group_dict['name']=group
  group_dict['description']=description
  group_dict['variables']=group_variables
  #print(f"Group Function: {json.dumps(group_dict)}")
  response=post_awx(f"/api/v2/inventories/{inv_id}/groups/",json.dumps(group_dict),awx,user,password)
  if response != "400 Bad Request":
    if response.status_code == 201:
      group_id=json.loads(response.text)['id']
  else:
    group_id=get_inv_group(group,inv_id,awx,user,password)
  return response, group_id

def add_inv_variables(inv_id,inv_variables,awx=awx,user=user,password=password):
  """Update the variables on an existing AWX inventory.

  Args:
      inv_id (int): The ID of the inventory to update.
      inv_variables (str): A JSON or YAML string of variables to assign to the
          inventory.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      requests.Response or None: The HTTP response from the PATCH request.
  """
  inv_dict={}
  inv_dict['variables']=inv_variables
  response=patch_awx(f"/api/v2/inventories/{inv_id}",json.dumps(inv_dict),awx,user,password)
  #print(f"Inventory Patch Function: {response.text} {json.dumps(inv_dict)}")
  return response

def add_org(orgname,description,ee_id,awx=awx,user=user,password=password):
  """Create a new organization in AWX.

  If the POST request returns a 400 Bad Request (indicating the organization
  already exists), the existing organization's ID is fetched via ``get_org``.

  Args:
      orgname (str): The name of the organization to create.
      description (str): A human-readable description for the organization.
      ee_id (int): The ID of the default execution environment for the
          organization.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created or existing organization (``0`` on failure).
  """
  org_id = 0
  org_dict={}
  org_dict['name']=orgname
  org_dict['description']=description
  org_dict['default_environment']=ee_id
  final_org=json.dumps(org_dict)
  response=post_awx("/api/v2/organizations/",final_org,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      org_id=json.loads(response.text)['id']
  else:
    org,org_id=get_org(orgname,awx,user,password)
  return response, org_id
  
def add_project(projname,description,org_id,ee_id,playbook_dir,awx=awx,user=user,password=password):
  """Create a new project within an AWX organization.

  If the POST request returns a 400 Bad Request (indicating the project already
  exists), the existing project's ID is fetched via ``get_project``.

  Args:
      projname (str): The name of the project to create.
      description (str): A human-readable description for the project.
      org_id (int): The ID of the organization that will own the project.
      ee_id (int): The ID of the default execution environment for the project.
      playbook_dir (str): The local path to the directory containing playbooks.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created or existing project (``0`` on failure).
  """
  proj_id = 0
  proj_dict={}
  proj_dict['name']=projname
  proj_dict['description']=description
  proj_dict['default_environment']=ee_id
  proj_dict['local_path']=playbook_dir
  final_proj=json.dumps(proj_dict)
  response=post_awx(f"/api/v2/organizations/{org_id}/projects/",final_proj,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      proj_id=json.loads(response.text)['id']
  else:
    project,proj_id=get_project(org_id,projname,awx,user,password)
  return response, proj_id


def add_job_template (project_id,inv_id,ee_id,job,extra_vars="",awx=awx,user=user,password=password):
  """Create a new job template in AWX.

  Merges the provided job JSON with references to the given project, inventory,
  extra variables, and execution environment before POSTing to the API.

  Args:
      project_id (int): The ID of the project to associate with the job
          template.
      inv_id (int): The ID of the inventory to associate with the job template.
      ee_id (int): The ID of the execution environment to use.
      job (str): JSON-encoded string representing the base job template data
          (must include at minimum a ``name`` and ``playbook`` key).
      extra_vars (str): A YAML or JSON string of extra variables to pass to the
          playbook. Defaults to an empty string.
      awx (str): Base URL of the AWX server. Defaults to the module-level
          ``awx`` value.
      user (str): AWX username. Defaults to the module-level ``user`` value.
      password (str): AWX password. Defaults to the module-level
          ``password`` value.

  Returns:
      tuple: A 2-tuple ``(requests.Response or str, int)`` containing:
          - The HTTP response from the POST request, or ``"400 Bad Request"``.
          - The ID of the created job template (``0`` if creation failed or
            returned 400).
  """
  job_template_id = 0
  job_dict=json.loads(job)
  job_dict["project"]=project_id
  job_dict["inventory"]=inv_id
  job_dict["extra_vars"]=extra_vars
  job_dict["execution_environment"]=ee_id
  final_job=json.dumps(job_dict)
  response=post_awx(f"/api/v2/job_templates/",final_job,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      job_template_id=json.loads(response.text)['id']
  return response, job_template_id 