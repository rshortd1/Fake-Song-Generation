import pandas as pd
import markovify
import tkinter as tk
from tkinter import ttk
import random
import re

# Load the CSV file
file_path = r"C:\Users\User\Desktop\Data\billboard_hot_100.csv"
data = pd.read_csv(file_path)

# Extract titles and performers
titles = data['title'].dropna().tolist()
performers = data['performer'].dropna().tolist()

# Combine titles and performers into separate strings
titles_text = " ".join(titles)
performers_text = " ".join(performers)

# Build the Markov chain models
title_model = markovify.Text(titles_text, state_size=1)
performer_model = markovify.Text(performers_text, state_size=1)

# Function to split names into syllables
def extract_syllables(name):
    return re.findall(r'[A-Za-z]+', name)

# Extract syllables from performer names
syllables = []
for performer in performers:
    syllables.extend(extract_syllables(performer))

# Deduplicate and filter syllables
syllables = list(set(syllables))
syllables = [syllable for syllable in syllables if len(syllable) > 2]

# Function to generate synthetic names
def generate_synthetic_name():
    num_syllables = random.choice([1, 2, 3])
    name = "".join(random.choices(syllables, k=num_syllables)).capitalize()
    return name[:12]  # Limit the length of the name

# Function to generate a sentence with length constraints
def generate_sentence(model, min_length=1, max_length=4):
    while True:
        sentence = model.make_sentence()
        if sentence:
            words = sentence.split()
            if min_length <= len(words) <= max_length:
                sentence = re.sub(r'[^\w\s]', '', sentence)  # Remove punctuation
                return " ".join(re.findall(r'\w+', sentence))  # Ensure spaces between words

# Function to generate a combination of artists
def generate_combined_artists(num_artists):
    connectors = ["feat.", "&", "and"]
    artists = [generate_synthetic_name() for _ in range(num_artists)]
    return f" {random.choice(connectors)} ".join(artists)

# Function to generate fake song names and artists
def generate_fake_songs():
    # Display loading message
    progress_label.config(text="Loading, please wait...")
    root.update_idletasks()

    # Generate 10 fake song names and artists
    fake_song_names_artists = []
    for _ in range(10):
        fake_title = generate_sentence(title_model)
        num_artists = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]  # Determine number of artists
        if num_artists == 1:
            fake_artist = generate_synthetic_name()
        else:
            fake_artist = generate_combined_artists(num_artists)
        fake_song_names_artists.append((fake_title, fake_artist))

    # Clear previous content
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Add headers
    rank_header = ttk.Label(table_frame, text="Rank", style="Header.TLabel")
    song_header = ttk.Label(table_frame, text="Song", style="Header.TLabel")
    artist_header = ttk.Label(table_frame, text="Artist", style="Header.TLabel")
    rank_header.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    song_header.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    artist_header.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    # Insert the generated fake song names and artists into the table frame
    for idx, (title, artist) in enumerate(fake_song_names_artists, start=1):
        bg_color = "lightgrey" if idx % 2 == 0 else "white"
        rank_label = ttk.Label(table_frame, text=f"{idx}", style="Rank.TLabel", background=bg_color)
        title_label = ttk.Label(table_frame, text=f"{title}", style="Title.TLabel", background=bg_color)
        artist_label = ttk.Label(table_frame, text=f"{artist}", style="Artist.TLabel", background=bg_color)
        
        rank_label.grid(row=idx, column=0, padx=5, pady=2, sticky='w')
        title_label.grid(row=idx, column=1, padx=5, pady=2, sticky='w')
        artist_label.grid(row=idx, column=2, padx=5, pady=2, sticky='w')

    # Hide loading message
    progress_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Fake Song Names and Artists")

# Add styling
style = ttk.Style()
style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
style.configure("Title.TLabel", font=("Helvetica", 12))
style.configure("Artist.TLabel", font=("Helvetica", 12))
style.configure("Rank.TLabel", font=("Helvetica", 12))

# Create a frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a progress label
progress_label = ttk.Label(main_frame, text="", style="Rank.TLabel")
progress_label.pack(pady=10)

# Create a frame for the table
table_frame = ttk.Frame(main_frame)
table_frame.pack(fill=tk.BOTH, expand=True)

# Generate and display fake songs after window is loaded
root.after(100, generate_fake_songs)

# Start the Tkinter event loop
root.mainloop()
