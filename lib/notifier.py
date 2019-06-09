import os

from typing import List

from sys import platform


class Notifier:
    def __init__(self, main_message="Repositories which are not up to date"):
        self.main_message = main_message
        self._notify = None

    @staticmethod
    def _notify_osx(title: str, body: str):
        os.system(
            f"""osascript -e 'display notification "{body}" with title "{title}"'"""
        )

    def notify(self, title: str, body: str):
        if not self._notify:
            if platform == "darwin":
                self._notify = self._notify_osx
            elif platform.startswith("linux"):
                from gi import require_version

                require_version("Notify", "0.7")
                from gi.repository import Notify

                def _notify_linux(title: str, body: str):
                    Notify.init(title)
                    n = Notify.Notification.new("", body)
                    n.set_urgency(Notify.Urgency.CRITICAL)
                    n.show()

                self._notify = self._notify_linux
            else:
                raise Exception("Not supported OS")
        return self._notify

    def send_notification(self, rows: List[str]):
        self.notify(self.main_message, "\n".join(rows))
