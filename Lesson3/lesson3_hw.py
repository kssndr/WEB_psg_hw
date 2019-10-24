import json
from lesson1_task1 import user
with open(f'user_{user}_repos_.json', 'r') as file: #открываем файл на чтение
    data = json.load(file) #загружаем из файла данные в словарь data

hw_tesk = open(f"lesson1_task_1_user_{user}.txt", "w")
hw_tesk.write("user " + user + " github repos list:"+"\n\n")
repos_total = 0
for i in data:
    hw_tesk.write(i["name"]+"\n")
    repos_total += 1

hw_tesk.write(f"\nTotal public repos: {repos_total}")
