# .PHONY говорит Make, что это названия команд, а не имена файлов
.PHONY: run build build-run update-app clean

# Локальный запуск через uv
start:
	uv sync
	uv run src/main.py

# Сборка образа
build:
	docker build -t backend-taskanline .

# Сборка + Запуск (зависит от build)
build-run: build
	docker run -d -p 8000:8000 --env-file ./.env -v taskanline_db:/app/database/ --name some-backend-taskanline backend-taskanline

run:
	docker start some-backend-taskanline

stop:
	docker stop some-backend-taskanline

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
