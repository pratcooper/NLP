from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize

stanford_dir = '/Users/prathameshnaik/Downloads/stanford-ner-2014-06-16/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.conll.4class.distsim.crf.ser.gz'

st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)

text = "John"
tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

print(classified_text[0][1])
