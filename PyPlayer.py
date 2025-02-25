import pygame
import os
import time
import random
import re
import select
import sys
import keyboard
import threading

# Initialize
pygame.mixer.init()

# 📁 Folder and library
music_folder = ""
songs = []
current_index = 0
is_playing = False
start_time = 0
volume = 100  # Hangerő százalékban
shuffle_songs = False
song_length = 0

# Load music
def load_music(file_path):
    global song_length
    pygame.mixer.music.load(file_path)
    song_length = pygame.mixer.Sound(file_path).get_length()
    time.sleep(1)

# Play music
def play_music():
    pygame.mixer.music.play()

# Stop music
def stop_music():
    pygame.mixer.music.stop()

# Pause music
def pause_music():
    pygame.mixer.music.pause()

# Continue music
def unpause_music():
    pygame.mixer.music.unpause()

# 🎶 Play music
def play_song():
    global is_playing, start_time, song_path
    if not songs:
        print("❌ No music loaded!")
        return
    
    is_playing = True
    start_time = time.time()

    song_path = os.path.join(music_folder, songs[current_index])

    # 🎛 Music control menu
    load_music(song_path)
    play_music()
    control_menu()

# 🎛 Control menu
def control_menu():
        while True:
            elapsed_time = int(pygame.mixer.music.get_pos() / 1000)
            elapsed_hours = elapsed_time // 3600
            elapsed_min = (elapsed_time % 3600) // 60
            elapsed_sec = elapsed_time % 60
            total_hours = int(song_length) // 3600
            total_min = (int(song_length) % 3600) // 60
            total_sec = int(song_length) % 60
            clear_terminal()
            print(f"Song title: {songs[current_index]}")
            sys.stdout.write(f"\nElapsed time: {elapsed_hours:02}:{elapsed_min:02}:{elapsed_sec:02} / {total_hours:02}:{total_min:02}:{total_sec:02}")
            print(f'\nVolume: {volume}%')
            print("\n🎛 Controls:")
            print("[N] Next  [P] Previous  [S] Stop  [+/-] Volume [Q] Quit")
            sys.stdout.flush()

            start_time = time.time()
            while time.time() - start_time < 1:
                if keyboard.is_pressed('n'):
                    clear_terminal()
                    print("Next song...")
                    next_song()
                if keyboard.is_pressed('P'):
                    clear_terminal()
                    print("Previous song...")
                    prev_song()
                    clear_terminal()
                if keyboard.is_pressed('s'):
                    clear_terminal()
                    pause_music()
                    stop_menu()
                if keyboard.is_pressed('+'):
                    change_volume(+10)
                    clear_terminal()
                if keyboard.is_pressed('-'):
                    change_volume(-10)
                    clear_terminal()
                if keyboard.is_pressed('q'):
                    clear_terminal()
                    exit_menu()

# ⏭ Next song
def next_song():
    global current_index, is_playing
    if not songs:
        return
    stop_music()  # Stop the previous song
    current_index = (current_index + 1) % len(songs)
    play_song()

# ⏮ Previous song
def prev_song():
    global current_index, is_playing
    if not songs:
        return
    stop_music()  # Stop the previous song
    current_index = (current_index - 1) % len(songs)
    play_song()

# 🧹 Clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# 🔊 Volume controls
def change_volume(amount):
    global volume
    volume = max(0, min(100, volume + amount))
    pygame.mixer.music.set_volume(volume / 100)  # Change the volume of pygame
    print(f"📢 Volume: {volume}%")
    time.sleep(0.1)
    clear_terminal()

# 📂 Select folder
def select_music_folder():
    global music_folder, songs, current_index
    clear_terminal()
    music_folder = input("📂 Path to folder: ").strip()

    if not os.path.isdir(music_folder):
        print("❌ Couldn't find folder!")
        time.sleep(2)
        return

    songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    if not songs:
        print("❌ There are no MP3 files in this folder!")
        time.sleep(2)
        return

    songs.sort(key=alphanumeric_sort)

    if shuffle_songs:
        random.shuffle(songs)
        current_index = random.randint(0, len(songs) - 1)
    else:
        current_index = 0

    play_song()

# Stop menu
def stop_menu():
    while True:
        clear_terminal()
        print("⏸️ Stop Menu")
        print("[1] Continue song")
        print("[2] Quit to main menu")

        choice = input("Választás: ").strip()
        if choice == "1":
            unpause_music()
            clear_terminal()
            control_menu()
        elif choice == "2":
            stop_music()
            print("Returning to main menu...")
            main_menu()

# 📄 Information
def show_info():
    clear_terminal()
    print("ℹ️ Information")
    print("🎵 Play MP3 files.")
    print("🎛 Controls: [N] Next, [B] Previous, [S] Stop, [+/-] Volume")
    print("🔀 Automatic playing, Shuffling")
    input("\nPress enter to go back...")

# 🎛 Main Menu
def main_menu():
    while True:
        clear_terminal()
        print("🎵 MP3 Player")
        print("[1] Play music")
        print("[2] Information")
        print("[3] Settings")
        print("[4] Quit")

        choice = input("Choice: ").strip()
        if choice == "1":
            select_music_folder()
        elif choice == "2":
            show_info()
        elif choice == "3":
            clear_terminal()
            settings_menu()
        elif choice == "4":
            clear_terminal
            print("👋 Goodbye!")
            time.sleep(2)
            exit()


# Settings menu
def settings_menu():
    global shuffle_songs
    while True:
        clear_terminal()
        print(f"Shuffle: {'ON' if shuffle_songs else 'OFF'}")

        print("⚙️ Settings")
        print("[1] Shuffle songs")
        print("[2] Return to main menu")

        choice = input("Choice: ").strip()
        if choice == "1":
            shuffle_menu()
        elif choice == "2":
            return

# Shuffle songs
def shuffle_menu():
    global shuffle_songs
    while True:
        clear_terminal()
        print(f"Enable shuffle?:")
        choice = input("\n[y/n]? ")
        if choice == "y":
            shuffle_songs = True
            break
        elif choice == "n":
            shuffle_songs = False
            break
        else:
            print("❌ Invalid input!")

# Sort songs in alphanumeric order
def alphanumeric_sort(file_name):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', file_name)]

# Exit menu
def exit_menu():
     while True:
        pause_music()
        if is_playing:
            print("❌ Music is still okaying!")
            print("Are you sure you want to quit? [y/n]")
            choice = input().strip().lower()
            if choice == "y":
                stop_music()
                clear_terminal
                exit()
            elif choice == "n":
                unpause_music()
                clear_terminal()
                control_menu()
            else:
                print("❌ Invalid input!")
                time.sleep(2)
                clear_terminal()
                control_menu()

# 🔄 Start program
if __name__ == "__main__":
    clear_terminal()
    main_menu()

