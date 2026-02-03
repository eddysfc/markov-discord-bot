import random
from collections import defaultdict, deque

MAX_HISTORY = 500


class MarkovChain:
    def __init__(self):
        self.model = defaultdict(list)
        self.history = deque(maxlen=MAX_HISTORY)

    def _get_pairs(self, text):
        words = text.split()
        for i in range(len(words) - 1):
            yield words[i], words[i + 1]

    def _remove_message(self, text):
        for w1, w2 in self._get_pairs(text):
            self.model[w1].remove(w2)
            if not self.model[w1]:
                del self.model[w1]

    def train(self, text):
        if len(self.history) == self.history.maxlen:
            oldest = self.history[0]
            self._remove_message(oldest)

        self.history.append(text)

        for w1, w2 in self._get_pairs(text):
            self.model[w1].append(w2)

    def generate(self, max_words=20):
        if not self.model:
            return None

        word = random.choice(list(self.model.keys()))
        output = [word]

        for _ in range(max_words - 1):
            next_words = self.model.get(word)
            if not next_words:
                break
            word = random.choice(next_words)
            output.append(word)

        return " ".join(output)
