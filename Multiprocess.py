import multiprocessing
import subprocess
import sys
import os

# Function to run a script
def run_script(script_name):
    try:
        # Execute the script using the current Python interpreter
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    # List of scripts to run
    scripts = [
        'FLASK_API.py',
        'Audio_uploader.py'
        # 'Audio_File_Reducer.py',
        # 'Audio_Uploader.py'
       
    ]

    # List to hold process objects
    processes = []

    for script in scripts:
        if os.path.exists(script):
            # Create a new process for each script
            p = multiprocessing.Process(target=run_script, args=(script,))
            processes.append(p)
            p.start()
        else:
            print(f"{script} not found!")

    # Wait for all processes to complete
    for p in processes:
        p.join()
