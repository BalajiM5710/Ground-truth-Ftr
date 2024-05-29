import streamlit as st
import os
import random
import pandas as pd

# Define the paths to the images directories
image_dirs = ["image1", "image2/image2"]

# Initialize session state to keep track of seen images and votes
if 'seen_images' not in st.session_state:
    st.session_state.seen_images = set()
if 'votes' not in st.session_state:
    st.session_state.votes = []

# List all images in both directories
image_files = []
for image_dir in image_dirs:
    image_files.extend([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))])

# Filter out images that have already been seen
unseen_images = [img for img in image_files if img not in st.session_state.seen_images]

# If all images have been seen, show a completion message and provide a download link for the CSV
if not unseen_images:
    st.write("All images have been voted on!")
    votes_df = pd.DataFrame(st.session_state.votes, columns=['file_name', 'voted_emotion'])
    csv = votes_df.to_csv(index=False)
    st.download_button(label="Download Votes CSV", data=csv, file_name="votes.csv", mime="text/csv")
else:
    # Randomly select an image from the unseen images
    current_image = random.choice(unseen_images)
    
    # Display the image
    st.image(current_image, use_column_width=True)
    
    # Define the voting function
    def vote(emotion):
        st.session_state.seen_images.add(current_image)
        st.session_state.votes.append((current_image, emotion))
        st.experimental_rerun()

    # Display voting buttons
    st.button('Happy', on_click=vote, args=('happy',))
    st.button('Sad', on_click=vote, args=('sad',))
    st.button('Neutral', on_click=vote, args=('neutral',))
    st.button('Angry', on_click=vote, args=('angry',))

# Optional: Display the current votes for debugging
# st.write(st.session_state.votes)
