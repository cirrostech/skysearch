from flask import Blueprint,render_template,request,jsonify
import requests,json
from requests.auth import HTTPBasicAuth

# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")
search_term = ""

base_url = "http://192.168.0.25:9200/"


headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}


@search_blueprint.route("/",methods=['GET', 'POST'],endpoint='index')
def index():

  if request.method == 'POST':
    print("POST")
    return render_template("index.html", search_term="Unlock")
  elif request.method == 'GET':
    return render_template("index.html")

@search_blueprint.route("/search",methods=['GET','POST'],endpoint='search')
def search():
  querystring = json.loads(request.data)
  print("Payload Body: {querystring}".format(querystring=querystring))
  
  search_term = querystring["query"]["search_term"]
  page_from = querystring["query"]["page_from"]

  print("Search Term:{search_term}".format(search_term=search_term))
  url = "http://192.168.0.25:9200"

  base_query = {
    "query_string": {
      "analyze_wildcard": True,
      "query": str(search_term),
			"fields": ["issue", "company"]
    }
  }

  agg_term = "Checking account"
  agg_query = {
    "bool": {
    	"must": [
        base_query,
        {
        	"match": {
            "sub_product": str(agg_term)
    	 		}
        }
    	]
    }
	}

  if request.method == 'POST':
    _from = 0
    str_query = base_query

  elif request.method == 'GET':
    _from = querystring
    str_query = agg_query
 
  payload = {
    "query":
     str_query , 
    "from": page_from,
    "size": 10,
    "sort": [],
    "aggs" : {
    	"sub_product" : {
        	"terms" : { "field" : "sub_product", "size": 100 }
    	}
	}
  }
  print("Payload {payload}".format(payload=payload))
  payload = json.dumps(payload)
  url = url + "/knowledgebase/_search"
  print("URL:{url}".format(url=url))
  response = requests.request("GET",url, data=payload, headers=headers)
#  print("Response {response}".format(response=response.text))
  response_dict_data = json.loads(str(response.text))
       
  return json.dumps(response_dict_data)


