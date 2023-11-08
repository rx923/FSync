import os
import sys
import shutil
import hashlib
import time

def synchronize_folders(source_folder, replica_folder, log_file_path):
    """
    Synchronize the replica folder's content to exactly match the source folder's content.

    Args:
        source_folder (str): Path to the source folder.
        replica_folder (str): Path to the replica folder.
        log_file_path (str): Path to the log file.
    """
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Open the log file for writing
    with open(log_file_path, "a") as log_file:
        # Walk through the source folder's directory structure
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))

                # Calculate MD5 hash of the source file
                with open(source_file_path, "rb") as source_file:
                    source_md5 = hashlib.md5(source_file.read()).hexdigest()

                # Calculate MD5 hash of the replica file if it exists
                if os.path.exists(replica_file_path):
                    with open(replica_file_path, "rb") as replica_file:
                        replica_md5 = hashlib.md5(replica_file.read()).hexdigest()
                else:
                    replica_md5 = None

                # Compare MD5 hashes and copy the file if they're different
                if source_md5 != replica_md5:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_entry = f"Copy: {source_file_path} -> {replica_file_path}"
                    log_file.write(log_entry + "\n")
                    print(log_entry)

        # Walk through the replica folder's directory structure using the built-in module of 'os'.
        for root, _, files in os.walk(replica_folder):
            # Iterating through the root, _ files in the replica_folder
            for file in files:
                # This for loop iterates through the files & data within the folder.
                # If the .txt files in the source_folder are present, it replicates the files in the replica_folder
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))

                # Remove replica file if it doesn't exist in the source folder
                if not os.path.exists(source_file_path):
                    # Removes the files
                    os.remove(replica_file_path)
                    log_entry = f"Remove: {replica_file_path}"
                    log_file.write(log_entry + "\n")
                    print(log_entry)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python sync_folders.py <source_folder> <replica_folder> <sync_interval> <log_file_path>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_file_path = sys.argv[4]

    while True:
        # Loop continues executing and analyzes for the operation of deletion/creation/modification of .txt files within the source folder.
        # Synchronization of the .txt files occurs at the set time duration while is being executed in CMD.
        synchronize_folders(source_folder, replica_folder, log_file_path)
        time.sleep(sync_interval)

# In order to run the code in command line, you have to use the below path:
#    Powershell: python.exe '.\Folder Synchronization.py' <path of the source_folder> <path of the replica_folder> <synchornization_interval of type int> <log_file_path.txt>




