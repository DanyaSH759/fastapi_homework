from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
import nest_asyncio
from pyngrok import ngrok
import uvicorn


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    # ваш код здесь
    return {"message": "Homework FastApi",
            "...": "Необходимо указать данные",
            
            "Добавление новой собаки": ["http://127.0.0.1:8000/dog_add?name=...&kind=..." , 
                                        "https://fastapi-homework-uqmi.onrender.com/dog_add?name=...&kind=..."],
            "Список всех собак": ["http://127.0.0.1:8000/dog_list",
                                  "https://fastapi-homework-uqmi.onrender.com/dog_list"],
                                  
            "Поиск собаки по id": ["http://127.0.0.1:8000/dog_id?id=...",
                                   "https://fastapi-homework-uqmi.onrender.com/dog_id?id=..."],
            
            "Поиск собак по породе": ["http://127.0.0.1:8000/dog_kind?kind=...", 
                                      "https://fastapi-homework-uqmi.onrender.com/dog_kind?kind=..."],
            
            "Измененеи данных о собаке по id": ["http://127.0.0.1:8000/dog_change_id?id=4&name=...&kind=...",
                                                "https://fastapi-homework-uqmi.onrender.com/dog_change_id?id=4&name=...&kind=..."],
            }]

# ваш код здесь

@app.post('/dog_add')
@app.get('/dog_add')
def dog_kind(name, kind):
    # Добавление собаки в список
    list_id = []
    for i in dogs_db:
        list_id.append(i)

    dogs_db[list_id[-1]+1] = Dog(name = name, pk=list_id[-1]+1, kind = kind)

    return f'Добавленная собака: {dogs_db[list_id[-1]+1]}', f'Список собак:', dogs_db


@app.post('/dog_list')
@app.get('/dog_list')
def dog_list():

    # список всех собак
    return dogs_db


@app.post('/dog_id')
@app.get('/dog_id')
def dog_id(id):

    # Поиск собаки по id 
    return dogs_db[int(id)]


@app.post('/dog_kind')
@app.get('/dog_kind')
def dog_kind(kind):

    # Поиск собак по породе
    lst = []

    # перебором ищем нужные записи
    for i in dogs_db:
        if dogs_db[i].kind == kind:
            lst.append(dogs_db[i])
    
    return lst


@app.post('/dog_change_id')
@app.get('/dog_change_id')
def dog_change(id, name = '', kind = ''):
    #Изменение собаки по id

    # данные до изменения
    change = dogs_db[int(id)]

    # если данных нет, то ничего не меняем
    if name == '' and kind == '':
        return 'Данные не изменены', dogs_db[int(id)]
    
    # если не заполнено имя, то меняем всё кроме него
    if name == '':
        dogs_db[int(id)] = Dog(name = dogs_db[int(id)].name, pk=id, kind = kind)
        return 'Исходные данные:', change, 'Данные изменены на:', dogs_db[int(id)]
    
    # если не заполнена порода, то меняем всё кроме неё
    if kind == '':
        dogs_db[int(id)] = Dog(name = name, pk=id, kind = dogs_db[int(id)].kind)
        return 'Исходные данные:', change, 'Данные изменены на:', dogs_db[int(id)]

    # иначе меняем всё
    dogs_db[int(id)] = Dog(name = name, pk=id, kind = kind)
    return 'Исходные данные:', change, 'Данные изменены на:', dogs_db[int(id)] 



# автоматически запуск api
#ngrok_tunnel = ngrok.connect(8000)
#print('Public URL:', ngrok_tunnel.public_url)
#nest_asyncio.apply()
#uvicorn.run(app, port=8000)
