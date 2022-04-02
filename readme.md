# Installation Instruction.

Table of content

# Setting up
1. Download and unzip the source code to the preferred location.
2. To setup the config file, open the config.py file and edit as appropriate.
3. Open SQL Server Management Studio and create your database using the database name as defined in the config file above.
4. Open the scripts folder and execute the procedure p_normalize_data.sql against the newly created database.
5. Download and install Python 3 SDK, prefarably 3.9.
6. Move files from *pcard-expenses* to the UNPROCESSED_FOLDER as defined in the config.py to prepare the processing.
7. Follow the next step to execute the program.

# Methods of Program Execution
There are numerous ways to install and execute this application. I will mention two methods.

## Method 1: Using PyCharm.
This program is developed using PyCharm, so we can download and install PyCharm. The following should be installed before proceeding.
1. Download and install PyCharm IDE.
2. Open this project by opening it via PyCharm by selecting Open and locating the source code folder.
3. Ensuring that main.py is the default starting file.
4. Going to the terminal in the window below, install the required dependecies using the following command:
   1. python -m pip install -r requirements.txt
5. After executing the above command successfully, click on **Run** to start the application.

## Method 2: Executing by command prompt.
1. Open the command prompt and navigate to the source code folder.
2. Once inside, run the following command without the *: *python main.py*
3. If it fails, create the virtual environment by running: *python3 -m venv venv*
4. Then execute the following:
   1. cd env\bin
   2. activate
5. Then install all the prerequisites listed in the requirement.txt file by executing the following command: *python -m pip install -r requirements.txt*
6. After all the requiements are successfully installed, execute this again: *python3 -m venv venv*
7. The program will start working and process files as long as the unprocessed folder is not empty.
8. Close the command prompt to stop the process.
 