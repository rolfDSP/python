"""Simple FastAPI app: enter text in a browser form and save it to textentered.txt.

If textentered.txt already exists, the text goes to resultingtext<N>.txt instead,
where N is one more than the highest number already used.
Text identical to the most recently saved file is not written again.

Several instances can run on different ports (PORT environment variable) and may
share one DATA_DIR: files are created exclusively, so no instance overwrites another.
"""

import os
import re
from pathlib import Path
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Folder for the text files; DATA_DIR can override it (used in the Docker container).
BASE_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
BASE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = BASE_DIR / "textentered.txt"
NUMBERED_PATTERN = re.compile(r"^resultingtext(\d+)\.txt$")

app = FastAPI()

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Favorite Text</title>
  <style>
    html, body {{ height: 100%; margin: 0; font-family: sans-serif; }}
    body {{ background: black; color: white; display: flex; flex-direction: column; align-items: center; padding: 1rem; box-sizing: border-box; }}
    form {{ display: flex; flex-direction: column; align-items: center; width: 100%; }}
    textarea {{ min-height: 50vh; min-width: 80vw; font-size: 1rem; padding: 0.5rem; box-sizing: border-box; }}
    .buttons {{ display: flex; gap: 1rem; }}
    button {{ margin-top: 1rem; padding: 0.5rem 2rem; font-size: 1rem; }}
    .msg {{ color: lightgreen; margin-top: 1rem; }}
  </style>
</head>
<body>
  <h1>Enter your favorite text here</h1>
  <form method="post" action="/">
    <textarea id="text" name="text">{text}</textarea>
    <div class="buttons">
      <button type="submit">Enter</button>
      <button type="button" onclick="clearText()">Clear</button>
    </div>
  </form>
  {message}
  <script>
    function clearText() {{
      const area = document.getElementById("text");
      area.value = "";
      area.focus();
      document.querySelector(".msg")?.remove();
    }}
  </script>
</body>
</html>
"""


def render(text: str = "", message: str = "") -> HTMLResponse:
    from html import escape

    msg_html = f'<p class="msg">{escape(message)}</p>' if message else ""
    return HTMLResponse(PAGE.format(text=escape(text), message=msg_html))


def next_numbered_file() -> Path:
    """Return resultingtext<N>.txt, with N one higher than the highest existing number."""
    numbers = [
        int(m.group(1))
        for f in BASE_DIR.iterdir()
        if (m := NUMBERED_PATTERN.match(f.name))
    ]
    return BASE_DIR / f"resultingtext{max(numbers, default=0) + 1}.txt"


def last_saved_file() -> Path | None:
    """Return the most recently written output file, or None if nothing was saved yet."""
    numbered = [
        (int(m.group(1)), f)
        for f in BASE_DIR.iterdir()
        if (m := NUMBERED_PATTERN.match(f.name))
    ]
    if numbered:
        return max(numbered)[1]
    return OUTPUT_FILE if OUTPUT_FILE.exists() else None


def save_new_file(text: str) -> Path:
    """Write text to the next free output file and return its path."""
    while True:
        target = next_numbered_file() if OUTPUT_FILE.exists() else OUTPUT_FILE
        try:
            # Mode "x" fails if the file already exists, so two instances
            # can never write to the same file.
            with target.open("x", encoding="utf-8") as f:
                f.write(text)
            return target
        except FileExistsError:
            continue  # another instance took this name first; pick the next one


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return render()


@app.post("/", response_class=HTMLResponse)
async def save_text(request: Request) -> HTMLResponse:
    # Parse the url-encoded form body directly (avoids the python-multipart dependency).
    body = (await request.body()).decode("utf-8")
    text = parse_qs(body, keep_blank_values=True).get("text", [""])[0]
    # Browsers send CRLF line endings; normalize so the comparison below matches.
    text = text.replace("\r\n", "\n")

    last = last_saved_file()
    if last is not None and last.read_text(encoding="utf-8") == text:
        return render(text, f"Text unchanged, already saved in {last.name}")

    target = save_new_file(text)
    return render(text, f"Text saved to {target.name}")


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 makes the page reachable from other machines on the local network.
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 6060)))
