# Expidle autosolver

Exponential Idle arrow puzzle autosolver

It uses cv2 to recognize circles and their colors on the screen. 
Ppadb is also used to connect to the phone (Android only). 
To write the algorithm, I used the official [guide](https://static.wikia.nocookie.net/exponential-idle/images/3/31/Exponential_Idle_Arrow_Puzzle_Guide_by_Eaux_Tacous.pdf/revision/latest?cb=20240603010745) for solving this puzzle.

## Installation and using

- Clone repository
- Create virtual environment (be sure you using **Python 3.8+**)
- Activate venv
- Install requirements 
    ```bash
    pip install -r requirements.txt
    ```
- Connect your phone to PC (you must enable USB debugging and allow input in the device system settings, under Developer options)
- Open Exponential Idle > Puzzles > Arrow Puzzle Hard/Expert
- Open solver.py, run
    ```python
    solve_puzzle_on_phone(max_color, times)
    ```
  Where max_color is the number of colors depending on the mode (Hard - 2, Expert - 6) and times is how many times do you want to solve the puzzle