import json
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

app = Flask(__name__)
cred = credentials.Certificate("creds/a2b3c4d-firebase-adminsdk-9hpl7-5905bde4d3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def build_response(status_code, message, data):
	response = dict()
	response['status_code'] = status_code
	response['message'] = message
	response['data'] = data

	return response


@app.route('/user/id=<userId>', methods=['GET', 'DELETE'])
def get_delete_user(userId = None):
	if request.method == 'DELETE':
		userId = userId
		data = list()

		users_ref = db.collection(u'users').stream()
			
		for doc in users_ref:
			if doc.to_dict()['userId'] == userId:
				db.collection(u'users').document(userId).delete()
				response = build_response(200, 'Success', data)
				return response

		response = build_response(400, 'userId not found', data)
		return jsonify(response)


	elif request.method == 'GET':
		userId = userId
		data = list()
	
		users_ref = db.collection(u'users')
		docs = users_ref.where(u'userId', u'==', userId).limit(1).stream()
	
		for doc in docs:
			data.append(doc.to_dict())

		if data == []:
			response = build_response(400, 'userId not found', data)
		else:
			response = build_response(200, 'Success', data)
		

		return (jsonify(response))


@app.route('/user/id=<userId>/fidelity')
def get_fidelity(userId = None):

	userId = userId
	data = list()

	users_ref = db.collection(u'users')
	docs = users_ref.where(u'userId', u'==', userId).stream()

	for doc in docs:
		data.append({'userId': doc.to_dict()['userId'], 'fidelity': doc.to_dict()['fidelity']})

	if data == []:
		response = build_response(400, 'userId not found', data)
	else:
		response = build_response(200, 'Success', data)
	
	return (jsonify(response))


@app.route('/user/id=<userId>/email')
def get_email(userId = None):
	userId = userId
	data = list()

	users_ref = db.collection(u'users')
	docs = users_ref.where(u'userId', u'==', userId).stream()

	for doc in docs:
		data.append({'userId': doc.to_dict()['userId'], 'email': doc.to_dict()['email']})

	if data == []:
		response = build_response(400, 'userId not found', data)
	else:
		response = build_response(200, 'Success', data)

	return (jsonify(response))


@app.route('/user/id=<userId>/isadmin')
def get_access_list(userId = None):

	userId = userId
	data = list()
	
	users_ref = db.collection(u'users')
	docs = users_ref.where(u'userId', u'==', userId).stream()

	for doc in docs:

		if doc.to_dict()['is_admin'] == True:
			response = build_response(200, 'Yes', data)
			return jsonify(response)

		elif doc.to_dict()['is_admin'] == False:
			response = build_response(200, 'No', data)
			return jsonify(response)

	response = build_response(400, 'userId not found', data)
	return jsonify(response)


@app.route('/user', methods=['POST'])
def post_create_user():
	if request.method == 'POST':

		data = list()
		email = request.form.get('email')
		userId = request.form.get('userId')

		if not email or not userId:
			response = build_response(400, 'bad written body', data)
			return response

		users_ref = db.collection(u'users')
		docs = users_ref.where(u'userId', u'==', userId).stream()

		# print(email, userId)

		for doc in docs:
			if userId == doc.to_dict()['userId']:
				response = build_response(409, 'userId already exists', data)
				return (jsonify(response))

		# add
		date_time = datetime.datetime.now()

		content = {'creation_date': date_time, 'email': email, 'fidelity': 0, 'is_admin': False, 'userId': userId}
		users_ref.document(userId).set(content)

		response = build_response(200, 'Success', data)
		
		return (jsonify(response))


@app.route('/user/id=<userId>/fidelity/increment', methods=['PATCH'])
def update_fidelity_increment(userId = None):
	if request.method == 'PATCH':
		userId = userId
		data = list()

		users_ref = db.collection(u'users').stream()

		for doc in users_ref:
			if doc.to_dict()['userId'] == userId:
				users_ref = db.collection(u'users').document(userId)
				users_ref.update({'fidelity': firestore.Increment(1)})
				response = build_response(200, 'Success', data)

				return jsonify(response)

		response = build_response(400, 'userId not found', data)
		return jsonify(response)


@app.route('/user/id=<userId>/fidelity/reset', methods=['PATCH'])
def update_fidelity_reset(userId = None):
	if request.method == 'PATCH':
		userId = userId
		data = list()

		users_ref = db.collection(u'users').stream()

		for doc in users_ref:
			if doc.to_dict()['userId'] == userId:
				users_ref = db.collection(u'users').document(userId)
				users_ref.update({'fidelity': 0})
				response = build_response(200, 'Success', data)

				return jsonify(response)

		response = build_response(400, 'user not found', data)
		return jsonify(response)


# GET

# /users
@app.route('/users')
def get_users():
	
	data = list()
	docs = db.collection(u'users').stream()

	for doc in docs:
		data.append(doc.to_dict())

	response = build_response(200, 'Success', data)
	return (jsonify(response))



# /transactions
@app.route('/transactions')
def get_transactions():
	
	data = list()
	docs = db.collection(u'transactions').stream()

	for doc in docs:
		data.append(doc.to_dict())

	response = build_response(200, 'Success', data)
	return (jsonify(response))


# /topics
@app.route('/topics')
def get_topics():
	
	data = list()
	docs = db.collection(u'topics').stream()

	for doc in docs:
		data.append(doc.to_dict())

	response = build_response(200, 'Success', data)
	return (jsonify(response))


# /products
@app.route('/products')
def get_products():
	
	data = list()
	docs = db.collection(u'products').stream()

	for doc in docs:
		data.append(doc.to_dict())

	response = build_response(200, 'Success', data)
	return (jsonify(response))


# /chats
@app.route('/chats')
def get_chats():
	
	data = list()
	docs = db.collection(u'chats').stream()

	for doc in docs:
		data.append(doc.to_dict())

	response = build_response(200, 'Success', data)
	return (jsonify(response))


# /transactions/id=<id>
@app.route('/transaction/id=<transactionId>', methods=['GET', 'DELETE'])
def get_delete_transaction(transactionId = None):
	if request.method == 'DELETE':
		transactionId = int(transactionId)
		data = list()

		docs = db.collection(u'transactions').stream()

		for doc in docs:
			if doc.to_dict()['transactionId'] == transactionId:
				db.collection(u'transactions').document(str(transactionId)).delete()
				response = build_response(200, 'Success', data)
				return response

		response = build_response(400, 'transaction not found', data)
		return jsonify(response)


	elif request.method == 'GET':
		transactionId = int(transactionId)
		data = list()
	
		db_ref = db.collection(u'transactions')
		docs = db_ref.where(u'transactionId', u'==', transactionId).limit(1).stream()
	
		for doc in docs:
			data.append(doc.to_dict())

		if data == []:
			response = build_response(400, 'transaction not found', data)
		else:
			response = build_response(200, 'Success', data)
		

		return (jsonify(response))


# /topics/id=<id>
@app.route('/topic/id=<topicId>', methods=['GET', 'DELETE'])
def get_delete_topic(topicId = None):
	if request.method == 'DELETE':
		topicId = int(topicId)
		data = list()

		docs = db.collection(u'topics').stream()

		for doc in docs:
			if doc.to_dict()['topicId'] == topicId:
				db.collection(u'topics').document(str(topicId)).delete()
				response = build_response(200, 'Success', data)
				return jsonify(response)

		response = build_response(400, 'topic not found', data)
		return jsonify(response)


	elif request.method == 'GET':
		topicId = int(topicId)
		data = list()
	
		db_ref = db.collection(u'topics')
		docs = db_ref.where(u'topicId', u'==', topicId).stream()
	
		for doc in docs:
			data.append(doc.to_dict())

		if data == []:
			response = build_response(400, 'topic not found', data)
		else:
			response = build_response(200, 'Success', data)
		

		return (jsonify(response))


# /products/id=<id>
@app.route('/product/id=<productId>', methods=['GET', 'DELETE'])
def get_delete_product(productId = None):
	if request.method == 'DELETE':
		productId = int(productId)
		data = list()

		docs = db.collection(u'products').stream()

		for doc in docs:
			if doc.to_dict()['productId'] == productId:
				db.collection(u'products').document(str(productId)).delete()
				response = build_response(200, 'Success', data)
				return response

		response = build_response(400, 'product not found', data)
		return jsonify(response)


	elif request.method == 'GET':
		productId = int(productId)
		data = list()
	
		db_ref = db.collection(u'products')
		docs = db_ref.where(u'productId', u'==', productId).stream()
	
		for doc in docs:
			data.append(doc.to_dict())

		if data == []:
			response = build_response(400, 'product not found', data)
		else:
			response = build_response(200, 'Success', data)
		

		return (jsonify(response))


# products/category=<category>
@app.route('/products/category=<category>')
def get_products_by_category(category = None):
	category = category
	data = list()
	docs = db.collection(u'products').where(u'category', '==', category).stream()

	for doc in docs:
		data.append(doc.to_dict())

	if data == []:
		response = build_response(400, 'category not found', data)
	else:
		response = build_response(200, 'Success', data)
	return (jsonify(response))


# /user/email=<email>/id
@app.route('/user/email=<email>/id')
def get_id_by_email(email = None):

	email = email
	data = list()

	users_ref = db.collection(u'users')
	docs = users_ref.where(u'email', u'==', email).stream()

	for doc in docs:
		data.append({'userId': doc.to_dict()['userId'], 'email': doc.to_dict()['email']})

	if data == []:
		response = build_response(400, 'email not found', data)
	else:
		response = build_response(200, 'Success', data)
	
	return (jsonify(response))


# POST

# /transaction
@app.route('/transaction', methods=['POST'])
def post_create_transaction():
	if request.method == 'POST':

		data = list()
		amount = float(request.form.get('amount'))
		productId = int(request.form.get('productId'))
		# string
		userId = request.form.get('userId')
		quantity = int(request.form.get('quantity'))
		transactionId = int(request.form.get('transactionId'))

		if not amount or not productId or not userId or not quantity or not transactionId:
			response = build_response(400, 'bad written body', data)
			return response

		db_ref = db.collection(u'transactions')
		docs = db_ref.where(u'transactionId', u'==', transactionId).stream()

		for doc in docs:
			if transactionId == doc.to_dict()['transactionId']:
				response = build_response(409, 'transaction with this id already exists', data)
				return (jsonify(response))

		# add
		date_time = datetime.datetime.now()

		content = {'amount': amount, 'date': date_time, 'productId': productId, 'quantity': quantity, 'transactionId': transactionId, 'userId': userId}
		db_ref.document(str(transactionId)).set(content)

		response = build_response(200, 'Success', data)
		
		return (jsonify(response))


# /topic
@app.route('/topic', methods=['POST'])
def post_create_topic():
	if request.method == 'POST':

		data = list()
		topicId = int(request.form.get('topicId'))
		name = request.form.get('name')

		if not name or not topicId:
			response = build_response(400, 'bad written body', data)
			return response

		db_ref = db.collection(u'topics')
		docs = db_ref.where(u'topicId', u'==', topicId).stream()

		for doc in docs:
			if topicId == doc.to_dict()['topicId']:
				response = build_response(409, 'topic already exists', data)
				return (jsonify(response))

		content = {'name': name, 'topicId': topicId}
		db_ref.document(str(topicId)).set(content)

		response = build_response(200, 'Success', data)
		
		return (jsonify(response))


# /product
@app.route('/product', methods=['POST'])
def post_create_product():
	if request.method == 'POST':

		data = list()

		url = request.form.get('URL')
		category = request.form.get('category')
		description = request.form.get('description')
		name = request.form.get('name')
		price = float(request.form.get('price'))
		productId = int(request.form.get('productId'))
		quantity = int(request.form.get('quantity'))
		specifications = request.form.get('specifications')

		if not category or not description or not name or not price or not productId or not quantity or not specifications or not url:
			response = build_response(400, 'bad written body', data)
			return response

		db_ref = db.collection(u'products')
		docs = db_ref.where(u'productId', u'==', productId).stream()

		for doc in docs:
			if productId == doc.to_dict()['productId']:
				response = build_response(409, 'product with this id already exists', data)
				return (jsonify(response))

		content = {'URL':url, 'category': category, 'description': description, 'name': name, 'price': price, 'productId': productId, 'quantity': quantity, 'specifications': specifications}
		db_ref.document(str(productId)).set(content)

		response = build_response(200, 'Success', data)
		
		return (jsonify(response))


# PATCH
# /products/quantity
@app.route('/product/quantity', methods=['PATCH'])
def update_product_cantity():

	if request.method == 'PATCH':
		data = list()

		productId = int(request.form.get('productId'))
		new_quantity = float(request.form.get('quantity'))

		if not productId or not new_quantity:
			response = build_response(400, 'bad written body', data)
			return response

		db_ref = db.collection(u'products').stream()

		for doc in db_ref:
			if doc.to_dict()['productId'] == productId:
				db_ref = db.collection(u'products').document(str(productId))
				db_ref.update({'quantity': new_quantity})
				response = build_response(200, 'Success', data)

				return jsonify(response)

		response = build_response(400, 'product not found', data)
		return jsonify(response)

# /products/price
@app.route('/product/price', methods=['PATCH'])
def update_product_price():

	if request.method == 'PATCH':
		data = list()

		productId = int(request.form.get('productId'))
		new_price = float(request.form.get('price'))

		if not productId or not new_price:
			response = build_response(400, 'bad written body', data)
			return response

		db_ref = db.collection(u'products').stream()

		for doc in db_ref:
			if doc.to_dict()['productId'] == productId:
				db_ref = db.collection(u'products').document(str(productId))
				db_ref.update({'price': new_price})
				response = build_response(200, 'Success', data)

				return jsonify(response)

		response = build_response(400, 'product not found', data)
		return jsonify(response)


# DELETE
# /transactions/id=<id>
# /topics/id=<id>
# /products/id=<id>
# /chats/id=<id>
if __name__ == '__main__':
	app.run(threaded=True)