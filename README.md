# Applicant tracking system

#### Requirements:-
* Python3.10+
* PostgreSQL 8.3+

## To Setup ats application please follow below steps:
1. Clone the repo using command `git clone https://github.com/Prem-Vk/webapp.git`
2. Create & activate virtualenv of python using below command.
	```
	python3.10 -m venv venv && source venv/bin/activate
	```
3. Install python requirements:- `pip install -r requirements.txt`
4. Run sql script to create a database using command:- `psql < setup_postgres.sql`
5. Running Migration `python manage.py migrate` . Note Migration will autofill Candidate Model using a custom migration script.
6. To run `python manage.py runserver 127.0.0.1:8080`.

### Test:
1. Create:
	```
	curl --request POST \
	  --url http://127.0.0.1:8080/api/candidates/7/ \
	  --data '{"name":"Priyanshu Gupta","age":36,"gender":"M","email":"as@gmail.com","phone_number":9769897698}'
	```
2. Delete:
	```
	curl --request DELETE \
	  --url http://127.0.0.1:8080/api/candidates/<id>/
	```
3. Update:
```
curl --request PUT \
  --url http://127.0.0.1:8080/api/candidates/<id>/ \
  --data '{"name":"Priyanshu Gupta","age":36,"gender":"M","email":"as@gmail.com","phone_number":9769897698}'
```
4. Relevance search:
```
curl --request GET \
  --url 'http://127.0.0.1:8080/api/candidates/?search=Ajay%20kumar%20yadav'
```
Thanks!!
<hr>