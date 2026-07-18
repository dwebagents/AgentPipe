import gc

def play_music():
    # Music playing logic
    pass

def cleanup():
    gc.collect()
    print("Memory reclaimed")

if __name__ == "__main__":
    play_music()
    cleanup()