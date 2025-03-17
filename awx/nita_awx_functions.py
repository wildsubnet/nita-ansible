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
      print ("post: "+awx+sub_url)
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
  return dict,0,"",0   

def get_job_templates (orgid,awx=awx,user=user,password=password):
  jobs=get_awx(f"/api/v2/organizations/{orgid}/job_templates",awx,user,password)
  job_templates=json.loads(jobs.text)
  return job_templates

def get_org (inventory_name,awx=awx,user=user,password=password):
  org=get_awx("/api/v2/organizations",awx,user,password)
  dictOrg=json.loads(org.text)
  for dict in dictOrg['results']:
    if dict['name'] == inventory_name:
      return dict,dict['id']  
  return dict,0

def get_project (orgid,awx=awx,user=user,password=password):
  response=get_awx(f"/api/v2/organizations/{orgid}/projects",awx,user,password)
  projects=json.loads(response.text)
  return projects

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
  print(final_ee)
  response=post_awx(f"/api/v2/execution_environments/",final_ee,awx,user,password)
  if response != "400 Bad Request":
    if response.status_code == 201:
      ee_id=json.loads(response.text)['id']
  else:
    ee_id,ee_desc,ee_env=get_ee(name,awx,user,password)

  return response, ee_id

def add_host (inventory_id, host_data, var_data,awx=awx,user=user,password=password):
  #Simple function to add a host to awx inventory 
  host_id = 0
  response=post_awx(f"/api/v2/inventories/{inventory_id}/hosts/",host_data,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      host_id=json.loads(response.text)['id']
      response=patch_awx(f"/api/v2/hosts/{host_id}/variable_data/",var_data,awx,user,password)
  return response, host_id

def add_inventory(orgid,invname,awx=awx,user=user,password=password):
  #Simple function to add Inventory to Project to awx 
  inventory_id = 0
  inventory_dict={}
  inventory_dict['name']=invname
  inventory_dict['description']=invname
  inventory_dict['organization']=orgid
  final_inventory=json.dumps(inventory_dict)
  print(inventory_dict)
  response=post_awx(f"/api/v2/inventories/",final_inventory,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      inventory_id=json.loads(response.text)['id']
  else:
    inv,inventory_id,inv_desc,inv_org=get_inventory(invname,awx,user,password) 
  return response, inventory_id  

def add_org(orgname,description,ee_id,awx=awx,user=user,password=password):
  #Simple function to add Organization to awx 
  org_id = 0
  org_dict={}
  org_dict['name']=orgname
  org_dict['description']=description
  org_dict['default_environment']=ee_id
  final_org=json.dumps(org_dict)
  print(final_org)
  response=post_awx("/api/v2/organizations/",final_org,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      org_id=json.loads(response.text)['id']
  else:
    org,org_id=get_org(orgname,awx,user,password)
  return response, org_id

def add_project(orgid,ee_id,project,awx=awx,user=user,password=password):
  #Simple function to add a host to Project to awx 
  project_id = 0
  project_dict=json.loads(project)
  project_dict['default_environment']=ee_id
  final_project=json.dumps(project_dict)
  print(final_project)
  response=post_awx(f"/api/v2/organizations/{orgid}/projects/",final_project,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      project_id=json.loads(response.text)['id']
  return response, project_id  

def add_job_template (project_id,job,awx=awx,user=user,password=password):
  #Simple function to add a host to add a Job Template
  job_template_id = 0
  job_dict=json.loads(job)
  job_dict["project"]=project_id
  final_job=json.dumps(job_dict)
  print(final_job)
  response=post_awx(f"/api/v2/job_templates/",final_job,awx,user,password)
  if response != "400 Bad Request":
     if response.status_code == 201:
      job_template_id=json.loads(response.text)['id']
  return response, job_template_id 