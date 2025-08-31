#  [CardioCare AI Suite](https://cardiocare-ai-suite.streamlit.app/)

This project is an interactive web application built with Streamlit that uses a machine learning model to predict the likelihood of heart disease. It features a multi-page portal for patient record management, doctor information, and hospital locations.

------------------------------------------------------------------------

## Required Files

To run this project, ensure you have all the following files in a single project folder:
- `HEART.py`  --- (The main application script)
- `PROM_model.pkl`  --- (The trained machine learning model)
- `heart.csv`  --- (The data-set used for training)
- `image_cac28b.png`  --- (The hospital banner image)
- `requirements.txt` --- (The list of required Python libraries)

------------------------------------------------------------------------

## Step-by-Step Instructions to Run the Application

Follow these steps carefully to set up and run the project on your local machine.


### Step 1: Download and Set Up the Project Files

1.  On the GitHub repository page **"Download ZIP"**.
2.  Find the downloaded ZIP file (e.g., `CardioCare-AI-Suite.zip`) in your Downloads folder.
3.  **Unzip** the downloaded file.

------------------------------------------------------------------------

### Step 2: Set Up the Python Environment

This step creates a dedicated, isolated environment for the project to avoid conflicts with other Python applications.

1.  Open the **Command Prompt** (on Windows) or **Terminal** (on macOS/Linux).

2.  Navigate into your project folder using the `cd` command.

    ``` bash
        cd path/to/your/CardioCare_Project
    ```
4.  Create a virtual environment by running:

    ``` bash
        python -m venv venv
    ```
    
5.  Activate the environment:
    * **On Windows:**
        
       ``` bash
        venv\Scripts\activate
        ```
        
    * **On macOS/Linux:** 
        
        ``` bash
        source venv/bin/activate
        ```
        
    You will know it's active when you see `(venv)` at the beginning of your command prompt line.

------------------------------------------------------------------------

### Step 3: Install Required Libraries

1.  Make sure your virtual environment is still active.

2.  Install all the necessary libraries at once by running the following command. 
    It reads the `requirements.txt` file and installs everything automatically. 
        
    ``` bash
        pip install -r requirements.txt
     ```
    
------------------------------------------------------------------------

### Step 4: Run the Application

1.  Ensure you are still in your project folder in the command prompt and the virtual environment is active.

2.  Launch the Streamlit application with this final command:  
        
    ``` bash
        streamlit run HEART.py
     ```

3.  A new tab will automatically open in your web browser with the running application.
