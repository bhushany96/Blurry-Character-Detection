The program is expected to output the text given in the image. The image can be noisy and some assumptions regarding noise were to be made.
##Emission Probability
Emission probability was calculated by comparing each and every pixel and checking number of pixels where there was "" in trainining data and in test letters and checking number of pixels where the pixel was " " in both train and test letters. Then, we decided to give more priority to former and after trying some possible combinations of values, we finally finalized to choose 0.9 where "" matched and 0.1 where "blank" matched. We stored all values in a dictionary and stored it using index values as keys. The count was calculated this way and then we calculated probability using modified laplace smoothing. I had to add 1 in numerator because some values were remaining zero.

##Transition Probability
Transition Probability was calcualted by iterating over the whole text string starting from the 1st letter as we would be checking the letter before that to compute the count of the current letter occuring after the previous letter. From this, we calculated the probability using Laplace smoothing.

##Initial Probability
Initial count was calculated by taking the count of the first letter from each sentence from "bc.train" file. From this, the initial probability was calculated by Laplace smoothing.

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
