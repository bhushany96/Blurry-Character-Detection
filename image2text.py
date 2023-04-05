#!/usr/bin/python

from PIL import Image, ImageDraw, ImageFont
import sys
import math
import numpy as np

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
train_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in
                    range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


def extract_data(fname):
    file = open(fname, 'r')
    data = []
    data_trans = []
    for line in file:
        data_list = [word for word in line.split()]
        data += [data_list]
        data_trans += [word for word in line]  # For extracting the data plus the spaces
    return data, data_trans


def initial_prob(data):
    init_prob = [0 for _ in range(len(train_letters))]
    word_count = 0
    for word_list in data:
        for word in word_list:
            word_count += 1
            if word[0] in train_letters:
                init_prob[train_letters.index(word[0])] += 1
    for i in range(len(train_letters)):
        init_prob[i] /= word_count
    return init_prob


def transition_prob():
    trans_prob = [[float(0) for _ in range(len(train_letters))] for _ in range(len(train_letters))]
  
    for i in range(len(data_trans)):
        if data_trans[i] in train_letters and data_trans[i+1] in train_letters:
            trans_prob[train_letters.index(data_trans[i])][train_letters.index(data_trans[i+1])] += 1
    #print(trans_prob)

    trans_prob_arr = np.array(trans_prob)
    for i in range(len(train_letters)):
        denom = sum(trans_prob_arr[i])
        for j in range(len(train_letters)):
            # Taking log as the transition probability is low
            if trans_prob_arr[i, j] != 0:
                trans_prob_arr[i, j] = math.log(float(trans_prob_arr[i, j]) / float(denom))
            else:
                trans_prob_arr[i, j] = math.log(1 / (float(denom) + 2))
    #print(trans_prob_arr)
    return trans_prob_arr


def emission_prob(train_letters_img, test_letters):
    emm_prob = [[0 for _ in range(len(train_letters_img))] for _ in range(len(test_letters))]
    noise = 0.4
    for letter in train_letters_img:
        for i in range(len(test_letters)):
            letter_img = train_letters_img.get(letter)
            for h in range(CHARACTER_HEIGHT):
                for w in range(CHARACTER_WIDTH):
                    if letter_img[h][w] == test_letters[i][h][w]:
                        if emm_prob[i][train_letters.index(letter)] == 0:
                            emm_prob[i][train_letters.index(letter)] = (1 - noise)
                        else:
                            emm_prob[i][train_letters.index(letter)] *= (1 - noise)
                    else:
                        if emm_prob[i][train_letters.index(letter)] == 0:
                            emm_prob[i][train_letters.index(letter)] = noise
                        else:
                            emm_prob[i][train_letters.index(letter)] *= noise
    return emm_prob


def simple(test_letters, emm_prob):
    simple_answer = ""
    for i in range(len(test_letters)):
        j = np.argmax(emm_prob[i])
        simple_answer += train_letters[j]
    return simple_answer


def veterbi(test_letters, init_prob, trans_prob, emm_prob):
    vet_table = [[0 for _ in range(len(test_letters))] for _ in range(len(train_letters))]
    fringe = [[0 for _ in range(len(test_letters))] for _ in range(len(train_letters))]
    actual_letter = [0 for _ in range(len(test_letters))]

    for i in range(len(train_letters)):
        vet_table[i][0] = init_prob[i] + math.log(emm_prob[0][i])

    for j in range(1, len(test_letters)):
        for i in range(len(train_letters)):
            temp = []
            for k in range(len(train_letters)):
                temp.append(vet_table[k][j - 1] + trans_prob[k, i] + math.log(emm_prob[j][i]))
            vet_table[i][j] = max(temp)
            fringe[i][j] = temp.index(vet_table[i][j])

    actual_letter[-1] = np.argmax(vet_table[:][-1])

    for i in reversed(range(1, len(test_letters))):
        actual_letter[i - 1] = fringe[actual_letter[i]][i]
    return actual_letter


(train_img_fname, train_txt_fname, test_img_fname) = './test_images/courier-train.png', \
                                                     './12345.txt',\
                                                     './test_images/test-2-0.png'
train_letters_img = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

# Below is just some sample code to show you how the functions above work.
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print("\n".join([ r for r in train_letters_img['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
# print("\n".join([r for r in test_letters[2]]))

# The final two lines of your output should look something like this:
data, data_trans = extract_data(train_txt_fname)
init_prob = initial_prob(data)
trans_prob = transition_prob()
emm_prob = emission_prob(train_letters_img, test_letters)
simple_answer = simple(test_letters, emm_prob)
print("Simple: " + simple_answer)
hmm_answer = veterbi(test_letters, init_prob, trans_prob, emm_prob)
print("   HMM: " + "".join([train_letters[i] for i in hmm_answer]))
