---------- READ ME ----------

For my project, I had started with trying to create a fully automated vehicle state machine for farming. I was shown a lot of the complexity of such a system.
Below are the instructions to run the program and some of the commands that are being called for each state. Thought this might be helpful to see and a short description of each of the state.

---------- How to Run ----------

    There are 2 ways to run this program:

    Option 1:

    1. Open the 'automated_farming.py' file in your perfered enviornment with the latest version of Python (Untested with previous Python releases).
    2. Run the file.
    3. Program should run through the field, but may become stuck. In such case, exit the program. "Ctrl + C" seemed to work best for me.

    Option 2:
    
    1. Navigate to the location of the project inside of command line.
    2. Inside of the project folder, type "python automated_farming.py".
    3. Program should run through the field, but may become stuck. In such case, exit the program. "Ctrl + C" seemed to work best for me.

    There are also files for "monte_carlo_search_tree.py" and "breadth_first_search.py", which happen to try and optimize routes. 
    They still have some bugs with them, but seem to give an idea on how these would work with automated farming. Run the same way, but with their respective files.

---------- Commands ----------

idle():
System will start from this command. Otherwise, nothing happens.
    1. start
        - drive()
    2. safety
        - safety()

drive():
Drives through field, but does not plant or harvest. Safer way of moving through the field.
    1. harvest
        - harvest()
    2. plant
        - plant()
    3. stop
        - idle()
    5. edge
        - edgeDetection()
    6. obstacle
        - obstacleDetection()
    7. safety
        - safety()
    8. continue
        - drive()

harvest():
Harvests field.
    1. drive
        - drive()
    2. stop
        - idle()
    3. edge
        - edgeDetection()
    4. obstacle
        - obstacleDetection()
    5. safety
        - safety()
    6. continue
        - harvest()

plant():
Plants field.
    1. drive
        - drive()
    2. stop
        - idle()
    3. edge
        - edgeDetection()
    4. obstacle
        - obstacleDetection()
    5. safety
        - safety()
    6. continue
        - plant()

obstacleDetection():
Detects obstacles and moves accordingly.
    1. drive
        - drive()
    2. harvest
        - harvest()
    3. plant
        - plant()
    4. stop
        - stop()
    5. safety
        - safety()

edgeDetection():
Detects edges and moves accordingly.
    1. drive
        - drive()
    2. harvest
        - harvest()
    3. plant
        - plant()
    4. stop
        - stop()
    5. safety
        - safety()

safety():
Similar to idle(), except here we do not want to start at all after coming into this state. This is more for errors mechanically or within the system.