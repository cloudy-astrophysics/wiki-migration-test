import sys
import re
from pathlib import Path
sys.path.append("../../../Source/tracboat/src/tracboat")
import trac2down

# Paths for reading input and saving output
try:
    input_path = Path(sys.argv[1])
    save_path = Path(sys.argv[2])
except (IndexError, ValueError, TypeError):
    sys.exit(f"Usage: {sys.argv[0]} INPUT_PATH SAVE_PATH")

# Get the names so that we can convert links to gollum format
# "CamelCaseName" -> "[[CamelCaseName]]"
wikinames = [p.name for p in input_path.glob("*")]


def fixup_wikilinks(text, targets):
    """Add double [[...]] around wikilinks (given as `targets`)

    Most prosaic method possible - simply loop over the explicit list
    of targets.  Tries to be careful in avoiding code blocks, but
    will still be fooled by inline code
    """
    lines = []
    is_code_block = False
    for line in text.split('\n'):
        # not blockquote?
        if not line.startswith('    '):
            if line.startswith("````"):
                is_code_block = not is_code_block
            if not is_code_block:
                for target in targets:
                    line = line.replace(target, f"[[{target}]]")
            # line = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'[[\1]]', line)
        lines.append(line)
    return "\n".join(lines)


# Process all the files in the input folder
for p in input_path.glob("*"):
    # Open file from the dump of the trac database and convert it
    with open(p) as f:
        text = trac2down.convert(f.read(), ".")
        text = fixup_wikilinks(text, wikinames)
    # Save the converted file with a ".md" extension to output folder
    # The 3rd, 4th, 5th arguments to this function are unused
    trac2down.save_file(text, p.name, None, None, None, save_path)
