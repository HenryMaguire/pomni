title: One Word Story (Part 1)
date: 23-10-2017
next: one_word_story_p2
picture: "http://via.placeholder.com/500x300"
summary: "Building a simple word game on the web using Flask."

# _One Word Story_
## Part 1 - _Building an AI story-telling game in Python_

In a [previous tutorial](/language_modelling/) I sowed the seeds necessary to implement a reasonably convincing language model. By this I mean we answered the question **given the prevous words in a sequence, what is the probability of word X being next?** in two different ways. The first way, was gathering descriptive statistics on some training text and allowing this to form the basis of conditional probability distributions. The problem we found with this method was that the model found it very difficult to _generalise_ from past examples. In other words, the likelihood of a given word appearing next was determined by whether it had appeared in that exact context in the training data so the model had no ability to choose a similar word in meaning unless this slightly different realisation had been seen already. This N-gram model was also difficult to improve without having prior knowledge of the way a language works, although I'm sure it would be possible to introduce word embeddings into the mix somehow.

To resolve the short-comings of the above model, we investigated a different approach using recurrent neural networks. Part of the standard architecture means that words are converted from a sparse _one-hot_ encoding into a distributed vector representation called embeddings. When trained effectively, these embeddings can learn the semantic and syntactical similarities between different words and so enable language models to interpolate between previous training examples in a higher-dimensional space. This method will also be applied to the problem of Machine Translation in later posts.

In order to increase our model's ability to learn deeper and more abstract qualities of the text we stacked multiple recurrent neural networks together. Dropout can then be introduced between layers to increase the robustness of the model by forcing it to learn the same representations of data in different ways across the network. The effect that different hyper-parameter regimes had on predictions were investigated in the previous post, here we will use this insight to choose an optimal architecture given the practical restrictions of building our word game.

## The Game
The players of each game are an AI and a human.
At the start of a game, one player will begin the story by inputting a word and the other player will give a word which it predicts is suitable to carry on the sentence. In the first iteration, each player will be able to give multiple words in each go. Punctuation can be suggested also, as part of or all of a go. For example: `"hello ` would then input `"` and `hello` into the game. I think that the bot will actually make two predictions - if the first prediction is a quotation/speech mark then it gets to say a word afterwards also. If the bot suggests a sentence ending punctuation (.!?) then it does not get to play another word. A story ends when either the bot yields an `END_OF_STORY` token, at which point it plays "THE END" or the human plays "THE END". I'll evaluate later whether or not the bot should indeed be given the right to finish stories.

## Settling on an architecture

**A few requirements of our application**

- Although we will train our model on a GPU, we may like to make predictions on a CPU so that it can eventually be run on a webserver (not sure how running a web app works yet).

- The AI will need to react to user input in real time. This means that predictions need to be fast to stop the user getting bored!

**Things to define**

- How to batch the data

- During training: feed in previously generated tokens or ground truth training data? Annealing between two?

- Hyperparameters (number of hidden units, dropout probability, number of layers, batch size)

- Greedy prediction or Beam Search?

##  Building the game in Python

Here define the platform of the game. Questions to consider:

- Who goes first?

- When does a story end?

- Is there a scoring system?

- What happens when the user gives a word the bot doesn't know?

- Will the bot greedily
