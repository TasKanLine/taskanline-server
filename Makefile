# .PHONY говорит Make, что это названия команд, а не имена файлов
.PHONY: run build build-run update-app clean

# Локальный запуск через uv
dev:
	uv sync
	uv run src/main.py

# Сборка образа
build:
	uv pip freeze > requirements.txt
	docker build -t backend-taskanline .

run:
	docker run -p 8000:8000 --name some-backend-taskanline -d backend-taskanline

build-run: build
	docker run -p 8000:8000 --name some-backend-taskanline -d backend-taskanline

start:
	docker start some-backend-taskanline

stop:
	-docker stop some-backend-taskanline

# Полное обновление: снос старого -> сборка -> запуск нового
# Мы просто вызываем другие цели по цепочке
update-app: clean
	git pull origin main
	build-run

# Очистка
clean: stop
	# Знак "-" перед командой означает "продолжить, даже если была ошибка"
	# (например, если контейнера нет, мы не хотим падать)
	-docker rm -f some-backend-taskanline
	-docker rmi backend-taskanline
