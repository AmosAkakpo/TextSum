import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

import spacy
import en_core_web_sm

nlp = spacy.load("en_core_web_sm")


class MyGrid(Widget):
    data = ObjectProperty(None)
    output_label=ObjectProperty(None)

    def preprocess_text(self, data):
        data2 = data.lower()
        doc = nlp(data2)
        
        newdoc1 = ' '.join([token.text for token in doc if not token.is_punct and not token.is_space and not token.is_stop])
        newdoc2 = [token for token in doc if not token.is_punct and not token.is_space]
        doc1 = nlp(newdoc1)

        return doc1

    def finding_frequencies(self, data):
        cleaned_text = self.preprocess_text(data)
        word_frequencies = {}
        for token in cleaned_text:
            word = token.text
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

        key_word = {}
        for word, frequency in word_frequencies.items():
            if frequency >= 2:
                if word not in key_word:
                    key_word[word] = frequency

        return key_word

    def calculating_score_for_sentences(self, data):
        doc = nlp(data)
        key_word = self.finding_frequencies(data)

        sentences_score = {}
        for sent in doc.sents:
            sentence_frequency = 0
            for token in sent:
                if token.text.lower() in key_word:
                    sentence_frequency += key_word[token.text.lower()]
            sentences_score[sent] = sentence_frequency

        max_score = max(sentences_score.values())

        for sentence, score in sentences_score.items():
            sentences_score[sentence] = score / max_score

        return sentences_score

    def output(self, data):
        doc = nlp(data)

        sentences_score = self.calculating_score_for_sentences(data)
        finaltext = ' '.join([sentence.text for sentence, score in sentences_score.items() if score >= 0.5])
        
        return finaltext

    def btn(self):
        summary= self.output(self.data.text)
        self.output_label.text = summary
    


class Myapp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    Myapp().run()
