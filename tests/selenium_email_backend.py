import os
from typing import Any

from django.conf import settings
from collections.abc import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from django.core.exceptions import ImproperlyConfigured



class SeleniumEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently: bool = ..., **kwargs: Any) -> None:
        super().__init__(fail_silently, **kwargs)
        self._fpath  = getattr(settings, 'EMAIL_FILE_PATH', None)
        self._filename = getattr(settings, 'EMAIL_FILENAME', None)
        try:
            os.makedirs(self._fpath, exist_ok=True)
        except FileExistsError:
            raise ImproperlyConfigured(
                f"Path for saving email messages exists, but is not a directory: {self._fpath}"
            )
        except OSError as err:
            raise ImproperlyConfigured(
                f"Could not create directory for saving email messages: {self._fpath} ({err})"
            )
        
    def send_messages(self, email_messages: Iterable[EmailMessage]) -> None:
        with open(os.path.join(self._fpath, self._filename), "w") as message:
            message.write(email_messages[0].body)
        return None
    