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
  inventories=get_awx("/api/v2/inventories",awx,user,password)
  dictInventory=json.loads(inventories.text)
  for dict in dictInventory['results']:
    if dict['name'] == inventory_name:
      return dict,dict['id'],dict['description'],dict['organization']  
  return dictInventory,0,"",0   

def get_inv_group (group_name,inventory_id,awx=awx,user=user,password=password):
  groups = get_awx(f"/api/v2/inventories/{inventory_id}/groups/",awx,user,password)
  groupsInv = json.loads(groups.text)
  for group in groupsInv['results']:
    if group['name'] == group_name:
      return group['id']
  return 0

def get_host (host_name,inventory_id,awx=awx,user=user,password=password):
  hosts = get_awx(f"/api/v2/inventories/{inventory_id}/hosts/",awx,user,password)
  hosts_inv = json.loads(hosts.text)
  for host in hosts_inv['results']:
    if host['name'] == host_name:
      return host,host['id']
  return hosts_inv,0

def get_job_templates (orgid,awx=awx,user=user,password=password):
  jobs=get_awx(f"/api/v2/organizations/{orgid}/job_templates",awx,user,password)
  job_templates=json.loads(jobs.text)
  return job_templates

def get_org (inventory_name,awx=awx,user=user,password=password):
  org=get_awx("/api/v2/organizations",awx,user,password)
  org_dict=json.loads(org.text)
  for dict in org_dict['results']:
    if dict['name'] == inventory_name:
      return dict,dict['id']  
  return dict,0

def get_project (orgid,name,awx=awx,user=user,password=password):
  projects=get_awx(f"/api/v2/organizations/{orgid}/projects",awx,user,password)
  project_dict=json.loads(projects.text)
  for dict in project_dict['results']:
    if dict['name'] == name:
      return dict,dict['id'],
  return dict,0

def get_ee(environment_name,awx=awx,user=user,password=password):
  #Retrieves the ID of an execution environment by its name.

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
  #Simple function to add EE to awx inventory 
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
  #Simple function to add a host to awx inventory 
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
  host_dict={}
  host_dict['id']=host_id
  final_group=json.dumps(host_dict)
  response=post_awx(f"/api/v2/groups/{group_id}/hosts/",final_group,awx,user,password)
  return response

def add_child_to_group (child_id,group_id,awx=awx,user=user,password=password):
  child_dict={}
  child_dict['id']=child_id
  final_group=json.dumps(child_dict)
  response=post_awx(f"/api/v2/groups/{group_id}/children/",final_group,awx,user,password)
  return response

def add_inventory(orgid,invname,awx=awx,user=user,password=password):
  #Simple function to add Inventory to Project to awx 
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
  inv_dict={}
  inv_dict['variables']=inv_variables
  response=patch_awx(f"/api/v2/inventories/{inv_id}",json.dumps(inv_dict),awx,user,password)
  #print(f"Inventory Patch Function: {response.text} {json.dumps(inv_dict)}")
  return response

def add_org(orgname,description,ee_id,awx=awx,user=user,password=password):
  #Simple function to add Organization to awx 
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
  #Simple function to add Organization to awx 
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
  #Simple function to add a host to add a Job Template
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