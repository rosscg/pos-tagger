# TODO remove multi-tags seperated with |, tags followed by $
# TODO document code
# TODO check type of data in probability frame - number of decimals

from Parser import Parser
import pandas as pd


class ProbabilityCounter:

    def __init__(self):
        print("Initialising probability counter...")

    def generate_cat_pr_table(self, data, smoothing):
        cat_count_df = self.cat_bigram_count(data)
        cat_pr_df = self.pr_dataframe(cat_count_df, smoothing)
        # print self.cat_pr_df.sum() # Check all probabilities sum to 1
        return cat_pr_df

    def generate_word_pr_table(self, data, smoothing):
        word_count_df = self.word_cat_count(data)
        word_pr_df = self.pr_dataframe(word_count_df, smoothing)
        # print word_pr_df.sum() # Check all probabilities sum to 1
        return word_pr_df

    def uniqify(self, seq):     # TODO move outside of this class? Is also called from main.save_data_values()
        # Uniqify, Not order preserving
        keys = {}
        for e in seq:
            keys[e] = 1
        return keys.keys()

    def cat_bigram_count(self, data):
        total_bigrams = 0   # TODO Can remove this
        cat_data = [x[1] for x in data]

        cat_unique = self.uniqify(cat_data)

        print("Number of unique category elements: %s" % len(cat_unique))

        cat_count_df = pd.DataFrame(0, index=cat_unique, columns=cat_unique) # TODO if SOS tag is not present but is added below, array will out of bounds

        print("Generating category count dataframe...")
        cat_prev = ''
        for cat in cat_data:
            if cat_prev== '':
                cat_prev = 'NN'  # TODO Change to start of sentence tag
            cat_count_df[cat_prev][cat] += 1
            total_bigrams += 1
            cat_prev = cat

        # print cat_count_df.to_string()
        print("Total Bigrams: %s" % total_bigrams)
        return cat_count_df

    def word_cat_count(self, data):
        cat_data = [x[1] for x in data]
        cat_unique = self.uniqify(cat_data)

        word_data = data
        word_unique = [x[0] for x in word_data]
        word_unique = self.uniqify(word_unique)

        word_count_df = pd.DataFrame(0, index=word_unique, columns=cat_unique) # TODO if SOS tag is not present but is added below, array will out of bounds

        print("Generating word-category count dataframe...")
        for word in word_data:
            word_count_df[word[1]][word[0]] += 1
        # print word_count_df.to_string()
        return word_count_df

    def pr_dataframe(self, data, smoothing):
        pr_df = data

        if smoothing:
            print("Performing add-one-smoothing...")
            pr_df += .1

        print("Calculating category probability dataframe...")
        for column in pr_df:
            col_sum = pr_df[column].sum()
            #print ("Column %s sum: %s" % (column, col_sum))
            pr_df[column] = pr_df[column] / col_sum

        # print pr_df.to_string()
        return pr_df


if __name__ == "__main__":
    path = 'text/test'
    data = Parser().parse_from_path(path)
    ProbabilityCounter().generate_cat_pr_table(data, 1)
    ProbabilityCounter().generate_word_pr_table(data, 1)
