import os
import pymongo
from flask import Flask, jsonify, request
from bson import ObjectId

host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database = os.getenv("MONGO_DATABASE")

client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
db = client[database]
books = db["books"]

app = Flask("library")

def parse_id(book):
	book["_id"] = str(book["_id"])
	return book

@app.route("/books", methods=["GET"])
def find_all():
	all_books = [parse_id(book) for book in books.find()]
	return (jsonify(all_books), 200)

@app.route("/books/<id>", methods=["GET"])
def find_by_id(id):
	book = books.find_one({"_id": ObjectId(id)})
	if not book:
		return ("", 404)
	book = parse_id(book)
	return (jsonify(book), 200)

@app.route("/books", methods=["POST"])
def insert():
	book = request.get_json()
	result = books.insert_one(book)
	id = {"_id": str(result.inserted_id)}
	return (jsonify(id), 201)

@app.route("/books/<id>", methods=["PUT"])
def update(id):
	book = request.get_json()
	book = books.find_one_and_update(
		{"_id": ObjectId(id)}, 
		{"$set": book},
		return_document=pymongo.ReturnDocument.AFTER
	)
	if not book:
		return("", 404)
	book = parse_id(book)
	return (jsonify(book), 200)

@app.route("/books/<id>", methods=["DELETE"])
def delete(id):
	result = books.delete_one({"_id": ObjectId(id)})
	if result.deleted_count < 1:
		return ("", 404)
	return ("", 204)

app.run(host="0.0.0.0", port=8000)
