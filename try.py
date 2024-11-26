import os
import shutil

# Set the directory where your PDF files are located
source_directory = "C:\\Users\\Pushpanjali\\Downloads" # Modify this path
destination_directory = 'C:\\Users\\Pushpanjali\\Desktop\\projects\\mcq\\English'  # Modify this path

# Create the 'Hindi' folder if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Loop through all files in the source directory
for filename in os.listdir(source_directory):
    # Check if the file is a PDF and contains 'HIN' in the name
    if filename.lower().endswith('.pdf') and 'eng' in filename.lower():
        # Full source and destination paths
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)
        
        # Move the file
        shutil.move(source_path, destination_path)
        print(f"Moved: {filename}")
