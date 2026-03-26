from flask import Flask, jsonify, request
from typing import List, Dict,Any
import os, json

customers_data:List[Dict[str,Any]]=[]
with open(os.path.join(os.path.dirname(__file__), "data", "customer.json"), "r", encoding="utf-8") as f:
    customers_data=json.loads(f.read())

app = Flask(__name__)

@app.route("/api/health",methods=["GET"])
def health_check():
    return jsonify(message="Health Check Successful"),200

@app.route("/api/customers/<customer_id>",methods=["GET"])
def get_single_customer(customer_id:str):
    try:
        customer={}
        for c in customers_data:
            if customer_id==c.get("customer_id"):
                customer=c
                break
        if not customer:
            return jsonify(message="Not Found"),404
        return jsonify(customer),200
    except Exception as e:
        return jsonify(message="Something went wrong",error=str(e)),500

@app.route("/api/customers",methods=["GET"])
def get_customer_data():
    try:
        page=int(request.args.get("page",1))
        limit=int(request.args.get("limit",10))
        offeset=(page-1)*limit
        return jsonify(data=customers_data[offeset:(offeset+limit)],page=page,limit=limit,total=len(customers_data)),200
    except Exception as e:
        return jsonify(message="Something went wrong",error=str(e)),500


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
