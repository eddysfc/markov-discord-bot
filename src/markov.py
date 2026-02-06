import random
from collections import defaultdict, deque
import json
from pathlib import Path
import re

MAX_HISTORY = 500
END_TOKEN = "<END>"
SAVE_PATH = Path("markov_data.json")


class MarkovChain:
    def __init__(self, order=2):
        self.model = defaultdict(list)
        self.history = deque(maxlen=MAX_HISTORY)
        self.order = order

    def _get_token_pairs(self, text):
        words = re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?|[^\w\s]", text)
        for i in range(len(words) - 1):
            yield words[i], words[i + 1]
        yield words[-1], END_TOKEN

    def _remove_message(self, text):
        for w1, w2 in self._get_token_pairs(text):
            self.model[w1].remove(w2)
            if not self.model[w1]:
                del self.model[w1]

    def train(self, text):
        words = text.split()
        if len(words) < self.order:
            return

        if len(self.history) == self.history.maxlen:
            oldest = self.history[0]
            self._remove_message(oldest)

        self.history.append(text)

        for w1, w2 in self._get_token_pairs(text):
            self.model[w1].append(w2)

    def generate(self, max_words=20):
        if not self.model:
            return None

        word = random.choice(list(self.model.keys()))
        output = [word]

        for _ in range(max_words - 1):
            next_words = self.model[word]
            if not next_words:
                break
            word = random.choice(next_words)
            if word == END_TOKEN and len(output) >= self.order:
                break
            output.append(word)

        message = " ".join(output)
        message = re.sub(r"\s+([.,!?;:])", r"\1", message)
        return message

    def save(self):
        with open(SAVE_PATH, "w") as f:
            json.dump(list(self.history), f)

    def load(self):
        if not SAVE_PATH.exists():
            return

        with open(SAVE_PATH, "r") as f:
            data = json.load(f)

        self.model.clear()
        self.history.clear()

        for message in data:
            self.train(message)
