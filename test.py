from requests import post, get, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(delete('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())

print(post('http://localhost:5000/api/v2/users', json={'surname': 'surname', 'name': 'name',
                                                         'age': 1, 'position': 'position',
                                                         'speciality': 'speciality',
                                                         'address': 'address', 'email':
                                                         'email'}).json())
print(get('http://localhost:5000/api/v2/users').json())
