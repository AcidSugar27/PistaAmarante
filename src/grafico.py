import time
import sys

def generate(name, total_time):

    track = ["🏎️"] + ["-"] * 20
    for i in range(1, len(track)):
        track[i-1] = "-"
        track[i] = "🚗"
        sys.stdout.write(f"\r{name}: {''.join(track)}")
        sys.stdout.flush()
        time.sleep(total_time / 20)

    sys.stdout.write(f" 🏁 ¡Terminó en {total_time:.4f} s!\n")
