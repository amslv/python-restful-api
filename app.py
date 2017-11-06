import flask
from flask import request, jsonify, session
import sqlalchemy
from sqlalchemy import inspect, desc
import json
import models
from models import engine, dbsession

@app.route("/<table_name>", methods=["POST", "PUT", "DELETE", "FETCH"])
def fetch(table_name):
    print("verb: %s, tablename: %s" % (request.method, table_name))
    if request.method == "POST" or request.method == "PUT":
        data = request.get_json(force=True)
        print("data:", data)
        try:
            TableClass = models.get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)
            if request.method == "POST": #insert data
                object = TableClass(**data)
                dbsession.add(object)
                dbsession.commit()
            else: #update data
                object = dbsession.query(TableClass).filter_by(**{"id":id}).first()
                if object == None: raise Exception("No data found.")
                for key in data.keys():
                    setattr(object, key, data[key])
                dbsession.commit()
            return jsonify({
                "status": "success",
                "id": object.id,
                })
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e),
                })
    elif request.method == "DELETE":
        try:
            TableClass = models.get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)
            object = dbsession.query(TableClass).filter_by(**{"id":id}).first()
            if object == None: raise Exception("No data found.")
            dbsession.delete(object)
            dbsession.commit()
            return jsonify({
                "status": "success",
                "id": object.id,
                })
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e),
                })
    elif request.method == "FETCH":
        try:
            data = request.get_json(force=True)
            data = json.loads(data)
            print("data: ", data)
            print("data-type: ", type(data))
            TableClass = models.get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)
            query = dbsession.query(TableClass).filter_by(**data['where'])
            if 'orderby' in data:
                for cname in data['orderby'].split(','):
                    reverse = False
                    if cname.endswith(' desc'):
                        reverse = True
                        cname = cname[:-5]
                    elif cname.endswith(' asc'):
                        cname = cname[:-4]
                    print("cname: ", cname)
                    column = getattr(TableClass, cname)
                    if reverse: column = desc(column)
                    query = query.order_by(column)
            if 'limit' in data:
                query = query.limit(data['limit'])
                query = query.offset(data['offset'])
            object = query.all()
            data = [object_as_dict(t) for t in object]
            return jsonify({
                "status": "success",
                "data": data
                })
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e),
                })
    else:
        return jsonify({
            "status": "error", "error": "Unrecognized verb.",
            })
