from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os

TASKS_FILE = "tasks.txt"
TASKS = []
NEXT_TASK_ID = 1


class TaskHandler(BaseHTTPRequestHandler):

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except:
            return None

    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, status, msg):
        self._send_json({"error": msg}, status=status)

    def _save_tasks(self):
        """Сохраняю задачу в файл"""
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "tasks": TASKS,
                    "next_id": NEXT_TASK_ID
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def do_POST(self):
        global NEXT_TASK_ID, TASKS

        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if parsed.path == "/tasks":
            # Создаю задачу
            data = self._read_json_body()

            if not data or "title" not in data or "priority" not in data:
                return self._error(400, "Fields 'title' and 'priority' are required")

            priority = data["priority"].lower()
            if priority not in ["low", "normal", "high"]:
                return self._error(400, "Priority must be 'low', 'normal' or 'high'")

            task = {
                "id": NEXT_TASK_ID,
                "title": data["title"],
                "priority": priority,
                "isDone": False
            }

            TASKS.append(task)
            NEXT_TASK_ID += 1
            self._save_tasks()
            self._send_json(task, 201)

        elif len(parts) == 3 and parts[0] == "tasks" and parts[2] == "complete":
            # Отмечаю, что задача выполнена
            try:
                task_id = int(parts[1])
            except:
                return self._error(400, "Task id must be integer")

            task_found = False
            for task in TASKS:
                if task["id"] == task_id:
                    task["isDone"] = True
                    task_found = True
                    break

            if task_found:
                self._save_tasks()
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()
            else:
                self._error(404, "Task not found")
        else:
            self._error(404, "Not found")

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/tasks":
            # Получаю список всех задач
            self._send_json(TASKS)
        else:
            self._error(404, "Not found")

    def log_message(self, fmt, *args):
        return


def load_tasks():
    """Загрузка задачи из файла при старте"""
    global TASKS, NEXT_TASK_ID

    if not os.path.exists(TASKS_FILE):
        TASKS = []
        NEXT_TASK_ID = 1
        return

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            TASKS = data.get("tasks", [])
            NEXT_TASK_ID = data.get("next_id", len(TASKS) + 1)
    except Exception:
        TASKS = []
        NEXT_TASK_ID = 1


def run(host="127.0.0.1", port=8085):
    print(f"Open on http://{host}:{port}")
    print(f"Loaded tasks: {len(TASKS)}")

    server = HTTPServer((host, port), TaskHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("The server is stopped")
        server.server_close()


if __name__ == "__main__":
    load_tasks()
    run()