from pathlib import Path
import subprocess

input_dir = Path("assets/audio")
output_dir = input_dir / "converted"
output_dir.mkdir(exist_ok=True)

for source in input_dir.glob("*.wav"):
    destination = output_dir / source.name

    command = [
        "ffmpeg",
        "-y",                  # overwrite output if it already exists
        "-i", str(source),
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        str(destination),
    ]

    print(f"Converting {source.name}...")
    subprocess.run(command, check=True)

print("Conversion complete.")