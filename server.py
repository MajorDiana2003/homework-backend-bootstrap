from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Задаем порт, на котором будет работать наш локальный сайт
PORT = 8000


class HomeworkServer(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка всех входящих GET-запросов"""

        # Если браузер запрашивает файл из папки /css/
        if self.path.startswith("/css/"):
            try:
                # Убираем первый слэш, чтобы получить путь 'css/bootstrap.min.css'
                file_path = self.path.lstrip("/")
                with open(file_path, "rb") as file:
                    css_content = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(css_content)
                return
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
                return

        # Для всех остальных запросов отдаем HTML
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        try:
            with open("contacts.html", "rb") as file:
                html_content = file.read()
            self.wfile.write(html_content)
        except FileNotFoundError:
            self.wfile.write(bytes("<h1>Файл contacts.html не найден!</h1>", "utf-8"))

    def do_POST(self):
        """Метод do_POST срабатывает, когда пользователь нажимает кнопку 'Отправить' в форме"""

        # Проверяем, что запрос пришел именно с формы контактов
        if self.path == "/contacts":

            # Читаем длину пришедших данных из заголовков запроса
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Распаковываем закодированную строку формы в удобный словарь (парсим данные)
            parsed_data = urllib.parse.parse_qs(post_data)

            # Критерий: Выводим данные формы в консоль PyCharm без ошибок
            print("\n==========================================")
            print("   ПОЛУЧЕНЫ НОВЫЕ ДАННЫЕ ИЗ ФОРМЫ СВЯЗИ   ")
            print("==========================================")
            for key, value in parsed_data.items():
                # Извлекаем значение из списка
                print(f"Поле '{key}': {value[0]}")
            print("==========================================\n")

            # После успешной обработки делаем перенаправление обратно на страницу контактов
            self.send_response(303)
            self.send_header("Location", "/contacts")
            self.end_headers()


# Функция для запуска самого сервера
def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HomeworkServer)
    print(f"🚀 Локальный сервер запущен! Открой в браузере: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем.")


if __name__ == "__main__":
    run()
