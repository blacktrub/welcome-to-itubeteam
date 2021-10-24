# Welcome to #itubeteam
Скрипт предназначен для автоматического добавления тега #itubeteam во все видео материала вашего YouTube канала

## Мотивация
- Автоматизация для каналов с большим количеством видео
- Легкий вход в сообщество

## Как это работает? 
Скрипт запрашивает ваш плейлист "загрузок" на канал, который содержит все ваши видео материалы. Затем скрипт проходится по каждому и проверяет есть тег #itubeteam, если тега нету, то добавляет его с помощью обновления данных о видео. 

## Предварительные действия
Так как скрипт использует YouTube API, то нельзя просто так взять и сходить в API, предварительно нужно завести Google приложение
- Создаем приложение https://console.cloud.google.com/projectcreate
- Добавляем доступ к YouTube https://console.cloud.google.com/apis/library/youtube.googleapis.com
- Заполняем данные для OAuth https://console.cloud.google.com/apis/credentials/consent
	- Экран: OAuth consent screen
		- Заполняем необходимые поля: App name, User support email, Developer info
	- Экран: Scopes
		- Нажимаем "Add or remove scopes"
		- В фильтре пишем youtube
		- Выбираем youtube.force-ssl
		- В таблице нажимаем галочку
		- Сохраняем с помощью Update
	- Экран: Test users
		- Добавляем Google аккаунт видео которого мы хотим обновлять
- Заводим credentials https://console.cloud.google.com/apis/credentials/oauthclient
	- Выбираем Application type: Desktop app
	- Нажимаем Create
	- Появится окно с успехом, нажимаем кнопку "Download json"
- Скаченный json нужно положить в директорию с кодом данного проекта и назвать secret.json
## Сборка и запуск
Проще всего запустить скрипт с помощью Docker контейнера
```bash
docker build -t welcome-script .
docker run -it welcome-script
```
После запуска скрипт предложит открыть страницу в браузере для получения OAuth кода авторизации, нужно открыть эту страницу, дать доступ нужному аккаунту и скопировать полученный авторизационный код в скрипт