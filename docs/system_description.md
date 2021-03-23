# Support Vector Machine on static word embeddings

The features for training and predicting are based solely on the reviewText field from the provided data. Any entry without a reviewText was determined to always return 1. The reviewText field is tokenized using NLTK's `word_tokenize` and then transformed to static word embeddings based on skip-gram embeddings trained on 2 billion words from English tweets. Finally, for each review, the mean of the collection of word embeddings is taken.

After processing the data, it is passed to a pipeline which Z-score standardizes the data and then finally, it is passed to an SVM with default scikit-learn parameters, except `max_iter=100000`.

It yielded an f1-score of roughly 0.9 on the dev set.