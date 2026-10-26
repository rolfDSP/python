"""ex042 - Adding two numbers.

A small FastAPI web application that adds two floating point numbers.
The HTML front end is reachable from any browser on the local network.

Run with:
    python main.py
then open http://<ip-of-this-machine>:8000 in a browser.
"""

from html import escape

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Adding two numbers")

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Calculating two numbers</title>
  <style>
    body {{
      background-color: #00008b;  /* dark blue */
      color: #ffffff;             /* white font */
      font-family: Arial, Helvetica, sans-serif;
      margin: 40px;
    }}
    label {{ display: inline-block; width: 140px; }}
    input[type=text] {{ width: 200px; padding: 4px; margin: 6px 0; }}
    button {{ margin-top: 12px; padding: 6px 20px; font-size: 1em; }}
    .error {{ color: #ffcccc; }}
  </style>
</head>
<body>
  <h1>Calculating two numbers</h1>
  <form method="get" action="/">
    <label for="first">First Number</label>
    <input type="text" id="first" name="first" value="{first}"><br>
    <label for="second">second number</label>
    <input type="text" id="second" name="second" value="{second}"><br>
    <label for="result">result</label>
    <input type="text" id="result" name="result" value="{result}" readonly><br>
    <button type="submit" name="op" value="add">Add</button>
    <button type="submit" name="op" value="sub">Subtract</button>
  </form>
  <p class="error">{error}</p>
</body>
</html>
"""


def add(a: float, b: float) -> float:
    """Return the sum of two floating point numbers."""
    return a + b

def sub(a: float, b: float) -> float:
    """return the difference of two floating point numbers."""
    return a - b


@app.get("/", response_class=HTMLResponse)
def index(first: str = "", second: str = "", op: str = "add") -> str:
    """Show the form; if both numbers are given, add or subtract them and show the result.

    `op` tells which button was pressed: "add" or "sub".
    """
    result = ""
    error = ""
    if first or second:
        try:
            # Accept a comma as decimal separator as well (e.g. "2,5").
            a = float(first.replace(",", "."))
            b = float(second.replace(",", "."))
            value = sub(a, b) if op == "sub" else add(a, b)
            result = f"{value:.3f}"
        except ValueError:
            error = "Please enter two valid numbers."
    return PAGE.format(
        first=escape(first),
        second=escape(second),
        result=escape(result),
        error=escape(error),
    )


if __name__ == "__main__":
    # 0.0.0.0 makes the server reachable from other machines on the local network.
    uvicorn.run(app, host="0.0.0.0", port=8000)
