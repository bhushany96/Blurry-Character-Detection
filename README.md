# Text-from-blurry-images
The program is expected to output the text given in the image. The image can be noisy and some assumptions regarding noise were to be made.
## Simple Bayes approach:
Calculate the max of the emission probability to check whether a letter matches any of the trained letter.
### Calculating Emission probability:
* Emission probability is basically the probability that a state has produced the variable to be predicted.
* Thus, in this case it will be the probability that the test letter matches the training set of letters.
* As the images have noise, a factor was to be considered according to the hint in the problem after checking the matches and mismatches of each pixel.
* This produced bad results. Thus, it was imperative to change the probabilities.
* If test pixel is * and training pixel is also * at a given point then the probability of matching is high rather higher than what was predicted before just by considering some noise value.
* Whereas if the test pixel is blank and training pixel is * then the probability of matching is way lower than the probability assumed by noise.
* Rest can be the same.
* This improved the output drastically on the positive side.

## Viterbi Approach:
In this transition probability is also considered on top of the emission probability and initial probabilities.
### Calculating Transition Probability:
* It the transition of every letter/character to another letter/character.
* All such transitions are counted for a particular letter and then divided by all transitions of that particular letter.
* In training set some transitions won't be available/trained. Thus, they will remain zero in the transition table.
* To avoid this Laplace smoothing is used.
