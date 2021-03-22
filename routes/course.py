"""Routes for the course resource.
"""
from datetime import datetime
from run import app
from flask import request
from flask import Response,jsonify
from http import HTTPStatus
import data
import json
import math
import re

@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    db = data.load_data()
    try:
        return Response(
            response=json.dumps({
                "data" : db[id] 
            }), 
            status=200, 
            mimetype="application/json"
        )
    except Exception as ex:
        print(db)
        return Response(
            response=json.dumps({
                "message" : "Course "+str(id)+" does not exist." 
            }), 
            status=404, 
            mimetype="application/json"
        )

@app.route("/course", methods=['GET'])
def get_courses():

    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    db = data.load_data_list()
    try:
        page_number = 1
        page_size = 10
        title_words = ""
        if(request.args.get("title-words")):
            title_words = request.args.get("title-words")
        if(request.args.get("page-number")):
            page_number = int(request.args.get("page-number"))
        if(request.args.get("page-size")):
            page_size = int(request.args.get("page-size"))

        total_pages = math.ceil(len(db)/page_size)
        if page_number>total_pages or page_number<1:
            return Response(
                response=json.dumps({
                    "message" : "Invalid pages" 
                }), 
                status=404, 
                mimetype="application/json"
            )    
        if title_words:
            print(True)
            result = []
            words = title_words.split(",")
            for i in range(0,len(db)):
                title = db[i]["title"]
                title = title.lower()
                count = 0
                for j in range(len(words)):
                    words[j] = words[j].lower()
                    if words[j] in title:
                        count += 1
                if count:
                    result.append([count,db[i]])
            res = []
            for i in result:
                res.append(i[1])
            result.sort(key=lambda x:x[0])
            return Response(
                response=json.dumps({
                    "data" : res[(page_number-1) * (page_size):min(page_number * page_size,len(db))]
                }), 
                status=200, 
                mimetype="application/json"
            )

        return Response(
            response=json.dumps({
                "data" : db[(page_number-1) * (page_size):min(page_number * page_size,len(db))] 
            }), 
            status=200, 
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps({
                "message" : "Invalid Pages." 
            }), 
            status=404, 
            mimetype="application/json"
        )




@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    db = data.load_data_list()
    try:
        if(request.form["description"] and request.form["title"] and request.form["discount_price"] and request.form["on_discount"] and request.form["price"] and request.form["image_path"]):
            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d, %H:%M:%S")
            new_course = {}
            new_course["date_created"] = now
            new_course["date_updated"] = now
            new_course["description"] = request.form["description"]
            new_course["title"] = request.form["title"]
            new_course["discount_price"] = float(request.form["discount_price"])
            new_course["price"] = float(request.form["price"])
            new_course["id"] = int(db[-1]["id"]) + 1
            new_course["image_path"] = request.form["image_path"]
            new_course["on_discount"] = bool(request.form["on_discount"])
            dat = jsonify({"data":new_course})
            return Response(
                response=json.dumps({
                    "data": new_course
                }), 
                status=200, 
                mimetype="application/json"
            )
        else:
            return Response(
            response=json.dumps({
                "message" : "All Parameters are not present!" 
            }), 
            status=500, 
            mimetype="application/json"
        )    
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({
                "message" : "Error occured!." 
            }), 
            status=500, 
            mimetype="application/json"
        )


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    db = data.load_data()
    
    try:
        print(db[id]) # prints the db item in the console and also if it is not present then rises and exception
        obj = db[id]

        if(request.form["description"] and request.form["title"] and request.form["discount_price"] and request.form["on_discount"] and request.form["price"] and request.form["image_path"]):
            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            obj["date_updated"] = now
            obj["description"] = request.form["description"]
            obj["title"] = request.form["title"]
            obj["discount_price"] = float(request.form["discount_price"])
            obj["price"] = float(request.form["price"])
            obj["image_path"] = request.form["image_path"]
            obj["on_discount"] = bool(request.form["on_discount"])
            return Response(
                response=json.dumps({
                    "data": obj
                }), 
                status=200, 
                mimetype="application/json"
            )
        else:
            return Response(
            response=json.dumps({
                "message" : "All Parameters are not present!" 
            }), 
            status=500, 
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({
                "message" : "Course "+str(id)+" does not exist." 
            }), 
            status=404, 
            mimetype="application/json"
        )


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    db = data.load_data()
    try:
        print(db[id]) # printing the course object in console as well as raising an exception if not found
        obj = db[id]
        del db[id]
        return Response(
            response=json.dumps({
                "message" : "The specified course is deleted!"
            }), 
            status=200, 
            mimetype="application/json"
        )
    except Exception as ex:
        print(db)
        return Response(
            response=json.dumps({
                "message" : "Course "+str(id)+" does not exist." 
            }), 
            status=404, 
            mimetype="application/json"
        )
