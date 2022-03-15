from requests import post, get, delete

'''Job Api'''
# get
print(get('http://localhost:5000/api/v2/jobs').json())  # Получим все работы
print(get('http://localhost:5000/api/v2/jobs/1').json())  # Получим существующую работу
print(get('http://localhost:5000/api/v2/jobs/999').json())  # Получим несуществующую работу

# delete
print(delete('http://localhost:5000/api/v2/jobs/1').json())  # Удалим существующую работу

print(get('http://localhost:5000/api/v2/jobs').json())  # Проверим удалилась ли она
print(get('http://localhost:5000/api/v2/jobs/1').json())  # Попробуем получить её

print(delete('http://localhost:5000/api/v2/jobs/99').json())  # Удалим несуществующую работу

print(get('http://localhost:5000/api/v2/jobs/99').json())  # Попробуем получить её

# post
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Some bebra', 'work_size': 25, 'collaborators': '1, 2',
                 'is_finished': True, 'team_leader': 1, 'start_date': '2022-01-1',
                 'end_date': '2000-1-1', 'categories': 'Bebra1, Bebra2'}).json())  # Создадим работу
print(get('http://localhost:5000/api/v2/jobs/3').json())  # Посмотрим на неё

# Попробуем не указать необходимый параметр team_leader
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Some bebra', 'work_size': 25, 'collaborators': '1, 2',
                 'is_finished': True, 'start_date': '2022-01-1',
                 'end_date': '2000-1-1', 'categories': 'Bebra1'}).json())
print(get('http://localhost:5000/api/v2/jobs/4').json())  # Проверим создался ли работа

# Попробуем не указать не необходимый параметр categories
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Some bebra 2.0', 'work_size': 25, 'collaborators': '1, 2',
                 'is_finished': True, 'start_date': '2022-01-1', 'team_leader': 4,
                 'end_date': '2000-1-1'}).json())
print(get('http://localhost:5000/api/v2/jobs/4').json())  # Проверим создался ли работа


'''User Api'''
# get
print(get('http://localhost:5000/api/v2/users').json())  # Получим всех пользователей
print(get('http://localhost:5000/api/v2/users/1').json())  # Получим существующего пользователя
print(get('http://localhost:5000/api/v2/users/999').json())  # Получим несуществующего пользователя

# delete
print(delete('http://localhost:5000/api/v2/users/1').json())  # Удалим существующего пользователя

print(get('http://localhost:5000/api/v2/users').json())  # Проверим удалился ли он
print(get('http://localhost:5000/api/v2/users/1').json())  # Попробуем получить его

print(delete('http://localhost:5000/api/v2/users/99').json())  # Удалим несуществующего пользователя

print(get('http://localhost:5000/api/v2/users/99').json())  # Попробуем получить его

# post
print(post('http://localhost:5000/api/v2/users', json={'surname': 'surname', 'name': 'name',
                                                       'age': 1, 'position': 'position',
                                                       'speciality': 'speciality',
                                                       'address': 'address', 'email':
                                                           'email'}).json())  # Создадим пользователя
print(get('http://localhost:5000/api/v2/users/5').json())  # Посмотрим на него
# Попробуем не указать необходимый параметр surname
print(post('http://localhost:5000/api/v2/users', json={'name': 'name',
                                                       'age': 1, 'position': 'position',
                                                       'speciality': 'speciality',
                                                       'address': 'address', 'email':
                                                           'email'}).json())
print(get('http://localhost:5000/api/v2/users/6').json())  # Проверим создался ли пользователь
