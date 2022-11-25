"""Script that matches transcript obtained from audio to the scripted show"""
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


def load_script(path: str) -> list:
    f = open(path, "r", encoding="utf-8")
    script = f.read()
    f.close()
    jokes = script.split("[JUMP]")
    return jokes


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def similarity(text1: str, text2:str) -> float:
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

stops = stopwords.words('spanish')

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words=stops)


def obtain_best_match_last_words(joke: str, transcript: list) -> (float,int):
    score = 0
    for i, line in enumerate(transcript):
        length = len(line)
        last_words = joke[-length:]
        current_score = similarity(line, last_words)
        if score < current_score:
            score = current_score
            best_index = i
    return [score, best_index]


def find_last_words(script: list, transcript: list, number_of_jokes: int) -> list:
    matches = []
    for joke_index, joke in enumerate(script):
        best_match = obtain_best_match_last_words(joke,transcript)
        matches.append(best_match+[joke_index])
    matches.sort(reverse=True)
    matches = matches[:number_of_jokes]
    result = [[transcript_index, joke_index] for score, transcript_index, joke_index in matches]
    result.sort()
    return result


def obtain_jokes(script: list,transcript: list, intervals: list, last_line_index: list) -> list:
    results = []
    previous_index = 0
    for i, index in enumerate(last_line_index):
        joke_dictionary = dict()
        joke_dictionary["script_joke"] = script[i]
        transcript_joke = ""
        for j in range(previous_index, index+1):
            transcript_joke += " " + transcript[i]
        joke_dictionary["transcript_joke"] = transcript_joke
        joke_dictionary["time_interval"] = [intervals[previous_index][1],intervals[index][0]]
        results.append(joke_dictionary)
    return results


def matching(transcript: list, intervals: list, script_path: str) -> list:
    """Matches transcript with planned script. The transcript is ordered by time and matches the intervals"""
    script = load_script(script_path)
    last_words_indexes = find_last_words(script, transcript, 4)
    script = [script[joke_index] for transcript_index, joke_index in last_words_indexes]
    last_line_index = [transcript_index for transcript_index, joke_index in last_words_indexes]
    full_jokes = obtain_jokes(script, transcript, intervals, last_line_index)
    return full_jokes
