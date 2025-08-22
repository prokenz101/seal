# seal
A fast and secure CLI password manager.

Runs in a terminal. Python IDLE is not recommended.

<br />

## Requirements
- Python 3.10+ recommended
- A dedicated terminal interface (e.g. `cmd`, `PowerShell (pwsh)`, or a Linux/MacOS terminal)
- Dependencies from [requirements.txt](https://github.com/prokenz101/seal/blob/main/requirements.txt)

<br />

## Installation
1. Get the code:
   - via GitHub CLI:
     - ```sh
       gh repo clone prokenz101/seal
       cd seal
       ```
   - via Git:
     - ```sh
       git clone https://github.com/prokenz101/seal
       cd seal
       ```
   - By downloading ZIP:
     - [Download the ZIP](https://github.com/prokenz101/seal/archive/refs/heads/main.zip) from the Code menu.
     - Extract it.
     - Open a terminal window inside the extracted folder.

2. Install dependencies:
   - ```sh
     pip install -r requirements.txt
     ```

<br />

## Using
Run:
```sh
python main.py
```
in the `seal` or `seal-main` folder with a dedicated terminal.

Notes:
- If you start it from IDLE, it will open a separate terminal and run there.
- If your terminal is too small, you may see: “Terminal window is too small to display text.” Resize and try again.

<br />

## Security
seal encrypts all stored secrets locally, but your security ultimately depends on the safety of your system and how you use the software. Use seal only in trusted environments with verified code. If your data is compromised, you are solely responsible.