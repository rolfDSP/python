# How to start and use "Adding two numbers"

## 1. Requirements

- Python 3.9 or newer
- The packages `fastapi` and `uvicorn`

Install them once with:

```bash
pip install -r requirements.txt
```

## 2. Start the application

Open a terminal in the project folder and run:

```bash
cd /home/rolf/python/env/src/ex042
python main.py
```

The server starts on port 8000 and reports something like:

```
Uvicorn running on http://0.0.0.0:8000
```

Leave the terminal open while you use the application.
Press `Ctrl+C` in this terminal to stop it.

## 3. Open the web page

- On the same computer: open <http://localhost:8000> in a browser.
- From another computer on the local network: open
  `http://<IP-address-of-this-computer>:8000`.
  You can find the IP address with `ip addr` (Linux) or `ipconfig` (Windows).

**Note for WSL2:** By default, other computers can't reach a server running
inside WSL2. Either turn on mirrored networking in WSL, or forward the port
on Windows (in an administrator PowerShell):

```powershell
netsh interface portproxy add v4tov4 listenport=8000 connectaddress=<WSL-IP> connectport=8000
```

and allow port 8000 through the Windows firewall.
Get the WSL IP address with `hostname -I` inside WSL.

## 4. Use the application

1. Type a number in the **First Number** field, for example `1.5`.
2. Type a number in the **second number** field, for example `2.25`.
3. Click one of the buttons:
   - **Add** calculates First Number + second number, for example `3.750`.
   - **Subtract** calculates First Number − second number, for example `-0.750`.
4. The result appears in the **result** field with 3 digits after the
   decimal point.

Notes:

- Both a dot and a comma work as the decimal separator (`2.5` or `2,5`).
- If an entry isn't a valid number, the page shows
  "Please enter two valid numbers."

## 5. Run the unit tests

The calculations are done by the functions `add()` and `sub()` in `main.py`.
Their unit tests are in `test_main.py` and use Python's built-in
`unittest` module, so nothing extra needs to be installed.

Open a terminal in the project folder and run:

```bash
cd /home/rolf/python/env/src/ex042
python -m unittest -v
```

The output lists each test and ends with `OK` when all tests pass:

```
test_floating_point_rounding (test_main.TestAdd...) ... ok
...
Ran 11 tests in 0.001s

OK
```

If a test fails, the output shows `FAILED` and which test failed.

If `pytest` is installed, `python -m pytest -v` runs the same tests.
