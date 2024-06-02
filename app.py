import streamlit as st
import os
import random
import pandas as pd
import hashlib

# Define the paths to the images directories
image_dirs = ["images1","image

# Path to the CSV file that stores votes
votes_csv_path = 'votes.csv'

# Load existing votes
if os.path.exists(votes_csv_path):
    votes_df = pd.read_csv(votes_csv_path)
    voted_images = set(votes_df['file_name'])
else:
    votes_df = pd.DataFrame(columns=['file_name', 'voted_emotion', 'voter_name'])
    voted_images = set()

# Initialize session state to keep track of votes and user chunk assignment
if 'votes' not in st.session_state:
    st.session_state.votes = []
if 'user_chunk' not in st.session_state:
    st.session_state.user_chunk = None

# List all images in the directories
image_files = []
for image_dir in image_dirs:
    image_files.extend([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))])

# Split images into chunks
num_chunks = 5
chunks = [image_files[i::num_chunks] for i in range(num_chunks)]

# Function to get the chunk index for a user
def get_chunk_index(username):
    return int(hashlib.md5(username.encode()).hexdigest(), 16) % num_chunks

# Input for the user's name
username = st.text_input("Enter your name:")
if username:
    chunk_index = get_chunk_index(username)
    st.session_state.user_chunk = chunks[chunk_index]
    
    # Filter out images that have already been voted on by this user
    unseen_images = [img for img in st.session_state.user_chunk if img not in voted_images]

    # Calculate the progress
    total_images = len(st.session_state.user_chunk)
    voted_images_count = total_images - len(unseen_images)
    
    # Display the progress
    progress = voted_images_count / total_images
    st.progress(progress)
    st.write(f"{voted_images_count}/{total_images} images have been voted on.")

    # If all images have been seen, show a completion message and provide a download link for the CSV
    if not unseen_images:
        st.write("All images have been voted on!")
        csv = votes_df.to_csv(index=False)
        st.download_button(label="Download Votes CSV", data=csv, file_name="votes.csv", mime="text/csv")
    else:
        # Randomly select an image from the unseen images
        current_image = random.choice(unseen_images)
        
        # Display the image
        st.image(current_image, use_column_width=True)
        
        # Define the voting function
        def vote(emotion):
            # Add the vote to the session state
            st.session_state.votes.append((current_image, emotion, username))
            # Update the votes CSV file
            new_vote_df = pd.DataFrame(st.session_state.votes, columns=['file_name', 'voted_emotion', 'voter_name'])
            updated_votes_df = pd.concat([votes_df, new_vote_df])
            updated_votes_df.to_csv(votes_csv_path, index=False)
            # Clear the current votes from session state
            st.session_state.votes = []
            st.experimental_rerun()

        # Display voting buttons
        st.button('Happy', on_click=vote, args=('happy',))
        st.button('Sad', on_click=vote, args=('sad',))
        st.button('Neutral', on_click=vote, args=('neutral',))
        st.button('Angry', on_click=vote, args=('angry',))
else:
    st.write("Please enter your name to start voting.")
