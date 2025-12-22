import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

YADISK_API = "https://cloud-api.yandex.net/v1/disk"


def get_ext_from_url(url: str) -> str:
    """
    Достаём расширение из пути URL (последняя часть после точки).
    Если не получается — вернём 'bin'.
    """
    try:
        path = urllib.parse.urlparse(url).path
    except Exception:
        return "bin"

    filename = path.rsplit("/", 1)[-1]
    if "." in filename and not filename.endswith("."):
        ext = filename.rsplit(".", 1)[-1].lower()
        # чуть-чуть фильтруем, чтобы не получилось странных расширений
        if ext and all(ch.isalnum() for ch in ext) and len(ext) <= 10:
            return ext
    return "bin"

def upload_by_url(token: str, file_url: str, disk_path: str):
    """
    Запуск загрузки по URL на Яндекс.Диск.
    Возвращает (status_code, text_response).
    """
    endpoint = f"{YADISK_API}/resources/upload"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"url": file_url, "path": disk_path}

    resp = requests.post(endpoint, headers=headers, params=params, timeout=20)
    return resp.status_code, resp.text

def get_uploaded_files(token: str) -> list:
    """
    Получаем список файлов в папке /Uploads на Яндекс.Диске.
    Возвращает список имён файлов.
    """
    endpoint = f"{YADISK_API}/resources"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": "/Uploads"}

    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            items = resp.json().get("_embedded", {}).get("items", [])
            return [item["name"] for item in items if item["type"] == "file"]
    except:
        pass
    return []

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: str, content_type: str = "text/plain; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path != "/":
            self._send(404, "not found")
            return

        # Безопасное получение токена
        token = getattr(self.server, 'token', None)
        if not token:
            self._send(500, "YADISK_TOKEN is not set")
            return

        uploaded_files = get_uploaded_files(token)

        files_html = ""
        for filename in uploaded_files:
            files_html += f'<li style="background-color: rgba(0, 200, 0, 0.25); padding: 5px; margin: 2px;">{filename}</li>'

        if not uploaded_files:
            files_html = '<li>Нет загруженных файлов</li>'

        html = f"""<!doctype html>
        <html>
        <body>
          <h2>Загруженные файлы:</h2>
          <ul>
            {files_html}
          </ul>
          <button id="btn">Загрузить по URL</button>

          <script>
            document.getElementById("btn").addEventListener("click", async () => {{
              const url = prompt("Введите URL файла:");
              if (!url) return;

              try {{
                const resp = await fetch("/download", {{
                  method: "POST",
                  headers: {{ "Content-Type": "text/plain; charset=utf-8" }},
                  body: url
                }});

                const text = await resp.text();
                alert(text);
                // ДОБАВИТЬ: автообновление страницы
                if (resp.ok) {{
                  setTimeout(() => location.reload(), 1000);
                }}
              }} catch (e) {{
                alert("Ошибка: " + e);
              }}
            }});
          </script>
        </body>
        </html>
        """
        self._send(200, html, "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/download":
            self._send(404, "not found")
            return

        token = getattr(self.server, 'token', None)
        if not token:
            self._send(500, "YADISK_TOKEN is not set")
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length)

        body_text = raw.decode("utf-8", errors="replace").strip()

        file_url = body_text

        if not file_url:
            self._send(400, "empty url")
            return
        if not (file_url.startswith("http://") or file_url.startswith("https://")):
            self._send(400, "url must start with http:// or https://")
            return

        ext = get_ext_from_url(file_url)
        ts = int(time.time())
        disk_path = f"/Uploads/{ts}.{ext}"

        status, yadisk_resp_text = upload_by_url(token, file_url, disk_path)

        self._send(
            status,
            f"disk_path={disk_path}\nstatus={status}\nresponse={yadisk_resp_text}\n",
        )

    def log_message(self, fmt, *args):
        return

def main():
    # Просим пользователя ввести токен
    token = input("Введите OAuth-токен для Яндекс.Диска: ").strip()
    if not token:
        print("Ошибка: Неверный токен.")
        return

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8080"))
    httpd = HTTPServer((host, port), Handler)
    httpd.token = token

    print(f"Open: http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()