from pathlib import Path # for path handling
from collections import Counter # counter is basically a more optimized dict for counting the number of instance of tokens
import os, re, unicodedata, sys, math # os for reading and writing to files, re for regex cleaning, unicode for removing accents, sys to use argv, math for calculating log probability

def strip_accents(string):
    return unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("ascii") # normalize() splits letter and accent, encode() converts it to ascii, decode() converts it back to python string

def clean_text(text):
    text = strip_accents(text)
    text = re.sub(r"[^A-Za-z0-9\s]+", " ", text) # regex, replace any string thats not alphanumeric with ""
    return text.lower() # convert to lower if upper

def createBOW(path, count):
    BOW = Counter()
    for entry in os.listdir(path):
        # print(f"{entry}")
        file_path = path / entry # get file's path
        if file_path.is_file():
            with open(file_path, "r", encoding="latin-1", errors="ignore") as text:
                BOW.update(clean_text(text.read()).split()) # cleans the text, then splits them, then adds them to counter
            count += 1
    return BOW, count


def log_p_message_given_class(word_counts, p_w_given_class, class_total_words, k, vocab_size):
    # Laplace-smoothed floor for unseen words in THIS class
    tiny_floor = k / (class_total_words + k * vocab_size)
    logp = 0.0
    for w, cnt in word_counts.items():
        pw = p_w_given_class.get(w, tiny_floor)
        logp += cnt * math.log(pw)
    return logp

# -- MAIN --

# checks if number of arguments is correct
if len(sys.argv) < 2:
    print("Usage: python carlos_exer5.py 'folder path'")
    sys.exit(1)

folder_path = sys.argv[1]

spamBOW = Counter()
hamBOW = Counter()
path = Path(folder_path) # path to folder
num_spam_msgs = 0
num_ham_msgs = 0

# make BOW for spam and ham
for entry in os.listdir(path):
    subfolder_path = path / entry
    if subfolder_path.is_dir():
        if subfolder_path.name == "spam": spamBOW, num_spam_msgs = createBOW(subfolder_path, 0)
        elif subfolder_path.name == "ham": hamBOW, num_ham_msgs = createBOW(subfolder_path, 0)
        else: continue
    else: continue

# get k value
while True:
    k_input = input("Please enter k-value: ")
    try:
        k = float(k_input)
        if k <= 0:
            print("The k-value must be a positive number.")
            continue
        break 
    except ValueError:
        print("Invalid input. The k-value must be a valid number (e.g., 1 or 0.001).")

vocabulary = set(spamBOW) | set(hamBOW) # set of words in both spam and ham
total_vocabulary = len(vocabulary) # number of unique words
spam_word_total = sum(spamBOW.values()) # number of words in total in spam
ham_word_total = sum(hamBOW.values()) # number of words in total in ham
total_count = spam_word_total + ham_word_total # number of words total

probability_spam = (num_spam_msgs + k) / (num_spam_msgs + num_ham_msgs + 2*k) # prior P(Spam) with laplace smoothing (k)
probability_ham = 1.0 - probability_spam # prior P(Ham)

# P(w|class)
probability_word_given_spam = dict()
probability_word_given_ham = dict()
for word in vocabulary:
    count_word_in_spam = spamBOW.get(word, 0)
    count_word_in_ham = hamBOW.get(word, 0)
    probability_word_given_spam[word] = (count_word_in_spam + k) / (spam_word_total + k * total_vocabulary)
    probability_word_given_ham[word] = (count_word_in_ham + k) / (ham_word_total + k * total_vocabulary)

with open(f"{path.name}_classification_results.txt", "w") as out:
    out.write("SPAM\n")
    out.write(f"Total Words: {sum(spamBOW.values())} \n")
    out.write(f"Dictionary Size: {len(spamBOW)}\n\n")
    
    out.write("HAM\n")
    out.write(f"Total Words: {sum(hamBOW.values())} \n")
    out.write(f"Dictionary Size: {len(hamBOW)}\n\n")
    # for word in sorted(wordCounter):
    #     out.write(f"{word}	{wordCounter[word]}\n")
    
    # classify folder
    classify_dir = path / "classify"
    for entry in sorted(os.listdir(classify_dir)):
        file_path = classify_dir / entry
        if not file_path.is_file():
            continue

        with open(file_path, "r", encoding="latin-1", errors="ignore") as fh:
            words = clean_text(fh.read()).split()
        message_counts = Counter(words)

        # log-likelihoods
        log_like_spam = log_p_message_given_class(message_counts, probability_word_given_spam, spam_word_total, k, total_vocabulary)
        log_like_ham  = log_p_message_given_class(message_counts, probability_word_given_ham,  ham_word_total,  k, total_vocabulary)

        # add log-priors
        log_post_spam = log_like_spam + math.log(probability_spam)
        log_post_ham  = log_like_ham  + math.log(probability_ham)
        # convert back from log space, use m and .exp to turn the biggest one to 1
        m = max(log_post_spam, log_post_ham)
        p_spam = math.exp(log_post_spam - m)
        p_ham  = math.exp(log_post_ham  - m)
        norm = p_spam + p_ham
        posterior_spam = p_spam / norm     # P(Spam | message)
        posterior_ham  = p_ham  / norm     # P(Ham  | message)

        predicted = "Spam" if posterior_spam >= 0.5 else "Ham"

        # filename, label, P(Spam|message)
        out.write(f"{entry}  {predicted:<4} {posterior_spam:.6g}\n")

print(f"Program successful! Please check {path.name}_classification_results.txt")