import requests
#-------login an user------- 
login_data = {
    'username': 'demo',
    'password': 'demo'
}

response = requests.post('http://localhost:5000/login', json=login_data)

if response.status_code == 200:
    result = response.json()
    print('Oturum açma başarılı.')
    print('Kullanıcı rolü:', result['role'])
else:
    print('Oturum açma hatası:', response.json())