from __future__ import annotations

import datetime
import subprocess
import sys
import threading
from pathlib import PurePath
from types import TracebackType
from typing import IO, Callable, List, Optional, TextIO, Type, Union

import shiny._utils

__all__ = (
    "ShinyAppProc",
    "run_shiny_app",
)


class OutputStream:
    """
    Designed to wrap an IO[str] and accumulate the output using a bg thread

    Also allows for blocking waits for particular lines.
    """

    def __init__(self, io: IO[str], desc: Optional[str] = None):
        self._io = io
        self._closed = False
        self._lines: List[str] = []
        self._cond = threading.Condition()
        self._thread = threading.Thread(
            group=None, target=self._run, daemon=True, name=desc
        )

        self._thread.start()

    def _run(self):
        """
        Add lines into self._lines in a tight loop.
        """

        try:
            while not self._io.closed:
                try:
                    line = self._io.readline()
                except ValueError:
                    # This is raised when the stream is closed
                    break
                if line != "":
                    with self._cond:
                        self._lines.append(line)
                        self._cond.notify_all()
        finally:
            # If we got here, we're finished reading self._io and need to signal any
            # waiters that we're done and they'll never hear from us again.
            with self._cond:
                self._closed = True
                self._cond.notify_all()

    def wait_for(self, predicate: Callable[[str], bool], timeout_secs: float) -> bool:
        """
        Wait until the predicate returns True for a line in the output.

        Parameters
        ----------
        predicate
            A function that takes a line of output and returns True if the line
            satisfies the condition.
        timeoutSecs
            How long to wait for the predicate to return True before raising a
            TimeoutError.
        """
        timeoutAt = datetime.datetime.now() + datetime.timedelta(seconds=timeoutSecs)
        pos = 0
        with self._cond:
            while True:
                while pos < len(self._lines):
                    if predicate(self._lines[pos]):
                        return True
                    pos += 1
                if self._closed:
                    return False
                else:
                    remaining = (timeoutAt - datetime.datetime.now()).total_seconds()
                    if remaining < 0 or not self._cond.wait(timeout=remaining):
                        # Timed out
                        raise TimeoutError(
                            "Timeout while waiting for Shiny app to become ready"
                        )

    def __str__(self):
        with self._cond:
            return "".join(self._lines)


def dummyio() -> TextIO:
    io = TextIO()
    io.close()
    return io


class ShinyAppProc:
    """
    Class that represents a running Shiny app process.

    This class is a context manager that can be used to run a Shiny app in a subprocess. It provides a way to interact
    with the app and terminate it when it is no longer needed.
    """

    proc: subprocess.Popen[str]
    """The subprocess object that represents the running Shiny app."""
    port: int
    """The port that the Shiny app is running on."""
    url: str
    """The URL that the Shiny app is running on."""
    stdout: OutputStream
    """The standard output stream of the Shiny app subprocess."""
    stderr: OutputStream
    """The standard error stream of the Shiny app subprocess."""

    def __init__(self, proc: subprocess.Popen[str], port: int):
        self.proc = proc
        self.port = port
        self.url = f"http://127.0.0.1:{port}/"
        self.stdout = OutputStream(proc.stdout or dummyio())
        self.stderr = OutputStream(proc.stderr or dummyio())
        threading.Thread(group=None, target=self._run, daemon=True).start()

    def _run(self) -> None:
        self.proc.wait()
        if self.proc.stdout is not None:
            self.proc.stdout.close()
        if self.proc.stderr is not None:
            self.proc.stderr.close()

    def close(self) -> None:
        """
        Closes the connection and terminates the process.

        This method is responsible for closing the connection and terminating the process associated with it.
        """
        # from time import sleep
        # sleep(0.5)
        self.proc.terminate()

    def __enter__(self) -> ShinyAppProc:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.close()

    def wait_until_ready(self, timeout_secs: float) -> None:
        """
        Waits until the shiny app is ready to serve requests.

        Parameters
        ----------
        timeout_secs
            The maximum number of seconds to wait for the app to become ready.

        Raises
        ------
        ConnectionError
            If there is an error while starting the shiny app.
        TimeoutError
            If the shiny app does not become ready within the specified timeout.
        """
        error_lines: List[str] = []

        def stderr_uvicorn(line: str) -> bool:
            error_lines.append(line)
            if "error while attempting to bind on address" in line:
                raise ConnectionError(f"Error while starting shiny app: `{line}`")
            return "Uvicorn running on" in line

        if self.stderr.wait_for(stderr_uvicorn, timeout_secs=timeout_secs):
            return
        else:
            raise TimeoutError(
                "Shiny app exited without ever becoming ready. Waiting for 'Uvicorn running on' in stderr. Last 20 lines of stderr:\n"
                + "\n".join(error_lines[-20:])
            )


def run_shiny_app(
    app_file: Union[str, PurePath],
    *,
    port: int = 0,
    cwd: Optional[str] = None,
    wait_for_start: bool = True,
    timeout_secs: float = 10,
    bufsize: int = 64 * 1024,
) -> ShinyAppProc:
    """
    Run a Shiny app in a subprocess.

    Parameters
    ----------
    app_file
        The path to the Shiny app file.
    port
        The port to run the app on. If 0, a random port will be chosen.
    cwd
        The working directory to run the app in.
    wait_for_start
        If True, wait for the app to become ready before returning.
    timeout_secs
        The maximum number of seconds to wait for the app to become ready.
    bufsize
        The buffer size to use for stdout and stderr.
    """
    shiny_port = port if port != 0 else shiny._utils.random_port()

    child = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "shiny",
            "run",
            "--port",
            str(shiny_port),
            str(app_file),
        ],
        bufsize=bufsize,
        executable=sys.executable,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        encoding="utf-8",
    )

    # TODO: Detect early exit

    sa = ShinyAppProc(child, shiny_port)
    if wait_for_start:
        sa.wait_until_ready(timeout_secs)
    return sa
