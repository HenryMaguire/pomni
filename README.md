# coding-blog
Blog written with Flask framework


# Blog contents

There will initially be two main themes:

- Machine Translation
- One word story app development: where a user writes
stories one (or a few) words at a time with a bot

Plan of posts will be:

**Intro to NLP and language modelling (single post)**
- Using Ngram conditional Probability distributions. Greedy vs. beam search.
- Failings of Ngram method. Lack of distributed representations, no sense of
closeness unless exact examples have been seen before.
- RNNs and learning long-distance dependencies. LSTMs.
- Vocabulary size contraints for Ngram vs. LSTM
- LSTM language model code. Making predictions - greedy vs. beam search.
- Multiple layers and the effects on fluency.

**Intro to Machine-Translation**
- Word embeddings and shared representations (post 1)
- Encoder-Decoder architecture overview(post 1)
- Adding complexity: (post 2)
  - forward vs. backward encoder inputs
  - Many layers
  - Bidirectionality
  - Attention mechanisms
  - Tokenising with respect to word roots to reduce vocab

**Building the one-word story app.**
- Creating the simple word game. LSTM makes predictions on entire past sequence (inputs from user and bot).
- Flask web application
- Using pre-trained speech recognition model to incorporate voice-activation. Argmax over vocab words becomes input into OWS app.
- Text to speech using a pre-trained model.

**And beyond...**
- Using images as a seed of _inspiration_ for the story bot or to generate pictorial descriptions/summaries of stories

## Improvements
- Decide on whether to make the content less Jargon-filled on the main website. 
