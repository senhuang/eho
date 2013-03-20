from behave import *
from random import choice, randint
from string import ascii_lowercase
from sys import path
from time import sleep

path.append(path.append(".."))

import RestApi
import json
rest = RestApi.RestApi()
global cluster_ids
cluster_ids = []

@When ('User see clusters')
def get_clusters(context):
    global status_code
    global res_content_list_clusters
    res_content_list_clusters = []
    res = rest.get_clusters()
    status_code = res.status_code
    if status_code == 200:
        res_content_list_clusters = json.loads(res.content)

@When ('User get cluster with id: "{n}"')
def get_cluster(context, n):
    global status_code
    global res_content_get_cluster
    res = rest.get_cluster(cluster_ids[int(n)])
    status_code = res.status_code
    if status_code == 200:
        res_content_get_cluster = json.loads(res.content)

@When('name: "{name}", im_id="{im_id}", jt_nn="{jt_nn}" & num="{num_jt_nn}", tt_dn="{tt_dn}" & num="{num_tt_dn}"')
def create_cluster_body(context, name, im_id, jt_nn, num_jt_nn, tt_dn, num_tt_dn):
    global cluster_body
    data = json.dumps(dict(
        cluster = dict(
            name = '%s' % (name),
            base_image_id = '%s' % (im_id),
            node_templates = {
                '%s' % str(jt_nn): num_jt_nn,
                '%s' % str(tt_dn): num_tt_dn,
            }
        )))
    cluster_body = data

@When ('User create cluster')
def add_cluster(context):
    global cluster_body
    global status_code
    global res_content
    res = rest.create_cluster(cluster_body)
    status_code = res.status_code
    if status_code == 202:
        #sleep(60)
        res_content = json.loads(res.content)
        cluster_ids.append(res_content['cluster'].get(u'id'))
    
@When ('User delete cluster with id: "{n}"')
def del_cluster(context, n):
    global status_code
    res = rest.delete_cluster(cluster_ids[int(n)])
    status_code = res.status_code

@When ('User put cluster with id: "{n}"')
def put_cluster(context, n):
    global status_code
    global res_content
    global cluster_body
    res = rest.create_cluster(cluster_body, cluster_ids[int(n)])
    status_code = res.status_code
    if status_code == 202:
        res_content = json.loads(res.content)
