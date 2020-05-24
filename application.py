import json
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
cred = credentials.Certificate("creds/a2b3c4d-firebase-adminsdk-9hpl7-5905bde4d3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# chats_ref = db.collection(u'chats')
# docs = chats_ref.stream()

# chats_list = []

# for doc in docs:
#     # chats_list.append(doc.to_dict())
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))

# print(chats_list)


@app.route('/user=<nickname>/fidelity')
def get_fidelity(nickname = None):

	nickname = nickname
	data = {'data' : []}
	print("nickname:", nickname)
	users_ref = db.collection(u'users')
	docs = users_ref.where(u'nickname', u'==', nickname).stream()

	for doc in docs:
		data['data'].append({'nickname': doc.to_dict()['nickname'], 'fidelity': doc.to_dict()['fidelity']})

	return (jsonify(data))


@app.route('/user=<nickname>/email')
def get_email(nickname = None):

	nickname = nickname
	data = {'data' : []}
	print("nickname:", nickname)
	users_ref = db.collection(u'users')
	docs = users_ref.where(u'nickname', u'==', nickname).stream()

	for doc in docs:
		data['data'].append({'nickname': doc.to_dict()['nickname'], 'email': doc.to_dict()['email']})

	return (jsonify(data))


@app.route('/user=<nickname>/access')
def get_access_list(nickname = None):

	nickname = nickname
	data = {'data' : []}
	print("nickname:", nickname)
	users_ref = db.collection(u'users')
	docs = users_ref.where(u'nickname', u'==', nickname).stream()

	for doc in docs:
		data['data'].append({'nickname': doc.to_dict()['nickname'], 'access': doc.to_dict()['has_admin_on']})

	return (jsonify(data))


@app.route('/user=<nickname>/access/topic=<topic>')
def get_if_access(nickname = None, topic = None):

	nickname = nickname
	topic = topic
	data = {'data' : []}
	print("nickname:", nickname)
	users_ref = db.collection(u'users')
	docs = users_ref.where(u'nickname', u'==', nickname).stream()

	for doc in docs:
		if topic in doc.to_dict()['has_admin_on'] or 'all' in doc.to_dict()['has_admin_on']:
			data['data'].append({'nickname': doc.to_dict()['nickname'], 'access': 'Yes'})
		else:
			data['data'].append({'nickname': doc.to_dict()['nickname'], 'access': 'No'})

	return (jsonify(data))


@app.route('/user', methods=['POST'])
def post_create_user():
	if request.method == 'POST':

		data = {'data' : []}
		dict(request.form)
		email = request.form.get('email')
		nickname = request.form.get('nickname')

		users_ref = db.collection(u'users')
		docs = users_ref.where(u'nickname', u'==', nickname).stream()

		# print(email, nickname)

		for doc in docs:
			if nickname == doc.to_dict()['nickname']:
				data['data'].append({'status_code': '400', 'message' : 'The name already exists'})
				print(data)
				return (jsonify(data))

		# add
		content = {'email': email, 'fidelity': 0, 'has_admin_on': [], 'nickname': nickname}
		users_ref.document(nickname).set(content)
		data['data'].append({'status_code' : '200', 'message' : 'Successful'})
		print(data)
		return (jsonify(data))


@app.route('/user=<nickname>/fidelity/increment', methods=['PATCH'])
def update_fidelity_increment(nickname = None):
	if request.method == 'PATCH':
		nickname = nickname
		data = {'data' : []}

		users_ref = db.collection(u'users').stream()

		for doc in users_ref:
			if doc.to_dict()['nickname'] == nickname:
				users_ref = db.collection(u'users').document(nickname)
				users_ref.update({'fidelity': firestore.Increment(1)})
				data['data'].append({'status_code' : '200', 'message' : 'Successful'})
				return data

		data['data'].append({'status_code': '400', 'message' : 'nickname not found'})
		return data


@app.route('/user=<nickname>/fidelity/reset', methods=['PATCH'])
def update_fidelity_reset(nickname = None):
	if request.method == 'PATCH':
		nickname = nickname
		data = {'data' : []}

		users_ref = db.collection(u'users').stream()

		for doc in users_ref:
			if doc.to_dict()['nickname'] == nickname:
				users_ref = db.collection(u'users').document(nickname)
				users_ref.update({'fidelity': 0})
				data['data'].append({'status_code' : '200', 'message' : 'Successful'})
				return data

		data['data'].append({'status_code': '400', 'message' : 'nickname not found'})
		return data


@app.route('/user=<nickname>', methods=['DELETE'])
def delete_user(nickname = None):
	if request.method == 'DELETE':
		nickname = nickname
		data = {'data' : []}

		users_ref = db.collection(u'users').stream()

		for doc in users_ref:
			if doc.to_dict()['nickname'] == nickname:
				db.collection(u'users').document(nickname).delete()
				data['data'].append({'status_code' : '200', 'message' : 'Successful'})
				return data

		data['data'].append({'status_code': '400', 'message' : 'nickname not found'})
		return data


if __name__ == '__main__':
	app.run(threaded=True)