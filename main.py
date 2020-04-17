import requests
import json
import argparse
import time


def input_data():
    parser = argparse.ArgumentParser(
        description="Запуск производится из консоли с ключом --id где нужно вставить id пользователя ВК."
                    "Перед началом работы поместите токен ВК в строку 25 файла main.py"
                    "\nРезультат работы программы представлен в файлах albums.txt, friends.txt,groups.txt,"
                    " где выводятся список альбомов, друзей и групп пользователя соответственно. Пример запуска: python main.py --id 42113378"
                    "\nБикоев Константин КН202 МЕН180207")
    parser.add_argument("--id", type=int, help="vk id")
    namespace = parser.parse_args()
    if namespace.id is None:
        raise Exception("Введите vk id")
    else:
        return namespace.id


class vkAPI:
    def __init__(self, vk_id):
        self.vk_id = str(vk_id)
        self.token = ""  # put your VK token
        self.groups = None
        self.friends = None
        self.albums = None
        self.notes = None
        self.get_info()

    def get_info(self):
        reqs = {
            'friends': ("friends.get", "fields=nickname&order=hints&"),
            'groups': ("groups.get", "extended=1&"),
            'photos': ("photos.getAlbums", ''),
            'notes': ("wall.get", 'filter=owner&extended=1&owner_id=' + self.vk_id)
        }
        self.groups = self.take_data_from_json(reqs['groups'][0], reqs['groups'][1])
        self.friends = self.take_data_from_json(reqs['friends'][0], reqs['friends'][1])
        self.albums = self.take_data_from_json(reqs['photos'][0], reqs['photos'][1])

    def take_data_from_json(self, command, params):
        json_data = requests.get(
            "https://api.vk.com/method/" + command +
            "?user_id=" + self.vk_id + "&" + params +
            "access_token=" + self.token + "&v=5.52").text
        data = json.loads(json_data)
        return data['response']['items']

    def output_groups(self):
        with open("groups.txt", 'w', encoding="UTF-8") as f:
            for i in range(len(self.groups)):
                group = self.groups[i]
                f.write(str(i + 1) + ") " + group['name'] + "\n")

    def output_friends(self):
        with open("friends.txt", 'w', encoding='UTF-8') as f:
            for i in range(len(self.friends)):
                friend = self.friends[i]
                name = " Имя: " + friend['first_name']
                last_name = "Фамилия: " + friend['last_name']
                f.write(str(i + 1) + ")" + name + '\n' + last_name + '\n\n')

    def output_albums(self):
        with open("albums.txt", 'w', encoding='UTF-8') as f:
            result = []
            for i in range(len(self.albums)):
                album = self.albums[i]
                creation_time_js_format = time.gmtime(album['created'])
                creation_time = "Дата создания: " + time.strftime('%H:%M:%S - %d-%m-%Y', creation_time_js_format)
                name = "Название: " + album['title']
                size = "Размер: " + str(album['size'])
                s = str(len(self.albums) - i) + ") " + creation_time + "\n" + name + "\n" + size + "\n\n"
                result.append(s)
            result = result[::-1]
            for album in result:
                f.write(album)


if __name__ == "__main__":
    vk_id = input_data()
    page = vkAPI(vk_id)
    page.output_friends()
    page.output_groups()
    page.output_albums()
