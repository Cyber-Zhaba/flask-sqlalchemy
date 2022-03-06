from requests import post, get, delete, put

print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(post('http://localhost:5000/api/users',
           json={'surname': 'surname', 'name': 'name', 'age': 1,
                 'position': 'position', 'speciality': 'speciality',
                 'address': 'address', 'email': 'email'}).json())
print(post('http://localhost:5000/api/users',
           json={'id': 6, 'surname': 'surname1', 'name': 'name1', 'age': 2,
                 'position': 'position1', 'speciality': 'speciality1',
                 'address': 'address1', 'email': 'email1'}).json())
print(post('http://localhost:5000/api/users',
           json={'id': 6, 'surname': 'surname', 'name': 'name', 'age': 1,
                 'position': 'position', 'speciality': 'speciality',
                 'address': 'address', 'email': 'email'}).json())
print(get('http://localhost:5000/api/users').json())
print(delete('http://localhost:5000/api/users/5').json())
print(get('http://localhost:5000/api/users').json())
print(post('http://localhost:5000/api/users',
           json={'surname': '', 'name': '', 'age': 0,
                 'position': '', 'speciality': '',
                 'address': '', 'email': ''}).json())
print(post('http://localhost:5000/api/users',
           json={'id': 6, 'surname': '', 'name': '', 'age': 0,
                 'position': '', 'speciality': '',
                 'address': '', 'email': ''}).json())
