import sys
from pathlib import Path
sys.path.append("../../../Source/tracboat/src/tracboat")
import trac2down

# Paths for reading input and saving output
try:
    input_path = Path(sys.argv[1])
    save_path = Path(sys.argv[2])
except (IndexError, ValueError, TypeError):
    sys.exit(f"Usage: {sys.argv[0]} INPUT_PATH SAVE_PATH")

# Loop over all files in the input folder
for p in input_path.glob("*"):
    # Open file from the dump of the trac database and convert it
    with open(p) as f:
        text = trac2down.convert(f.read(), ".")
    # Save the converted file with a ".md" extension to output folder
    # The 3rd, 4th, 5th arguments to this function are unused
    trac2down.save_file(text, p.name, None, None, None, save_path)
