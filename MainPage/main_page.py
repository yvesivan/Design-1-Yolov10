import streamlit as st
from ImagedGathered import IG
from Location import Loc
from Uploads import Upload

# Set up the main page with background and buttons
def main_page():
    st.image("Backgrounds/bg2.png", use_column_width=True)
    
    st.title("Main Page")
    
    # Create buttons for navigation
    if st.button("Image Gathered"):
        IG.main_page()  # Navigate to IG.py's main_page
    
    if st.button("Location"):
        Loc.main_page()  # Navigate to Loc.py's main_page
    
    if st.button("Upload"):
        Upload.main_page()  # Navigate to Upload.py's main_page

# Entry point for the main page
if __name__ == "__main__":
    main_page()
