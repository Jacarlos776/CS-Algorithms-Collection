from pathlib import Path # for path handling
from collections import Counter # counter is basically a more optimized dict for counting the number of instance of tokens
import os, re, unicodedata, sys # os for reading and writing to files, re for regex cleaning, unicode for removing accents, sys to use argv

def strip_accents(string):
    return unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("ascii") # normalize() splits letter and accent, encode() converts it to ascii, decode() converts it back to python string

def clean_text(text):
    text = strip_accents(text)
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text) # regex, replace any string thats not alphanumeric with ""
    return text.lower() # convert to lower if upper

# checks if number of arguments is correct
if len(sys.argv) < 2:
    print("Usage: python carlos_exer4.py 'folder path'")
    sys.exit(1)

folder_path = sys.argv[1]

# print(f"{folder_path}")
wordCounter = Counter() # where we'll store the words
path = Path(folder_path) # path to folder
# print(f"{path}")
for entry in os.listdir(path):
    # print(f"{entry}")
    file_path = path / entry # get file's path
    if file_path.is_file():
        with open(file_path, "r", encoding="latin-1", errors="ignore") as text:
            wordCounter.update(clean_text(text.read()).split()) # cleans the text, then splits them, then adds them to counter

with open("output.txt", "w") as out:
    out.write(f"Total Words in {path.name}: {sum(wordCounter.values())} \n")
    out.write(f"Dictionary Size ({path.name}): {len(wordCounter)}\n\n")
    for word in sorted(wordCounter):
        out.write(f"{word}	{wordCounter[word]}\n")
        
print("Program successful! Please check output.txt")