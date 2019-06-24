from ProbabilityCounter import ProbabilityCounter
from Parser import Parser
from Viterbi import Viterbi
import time


class Main:

    def __init__(self):
        path = 'text/test'
        start_time = time.time() #Uses wall time rather than processor time, which would be time.clock()
        clock_time = time.clock() #Clock time.
        data = Parser().parse_from_path(path)

        self.save_data_values(data)
        self.test_known_words(data) #TODO run both methods and store and compare values
        #self.test_unknown_words(data)

        print('Total Run Time: %.1f minutes' % ((time.time() - start_time)/60))
        print('Total Clock Time: %.1f minutes' % (time.clock() - clock_time))


    def test_known_words(self, data):

        total_observations = 0
        wrong_count = 0

        test_data = data
        training_data = data

        total_observations_to_add, wrong_count_to_add = self.run_viterbi(test_data, training_data, 0)
        total_observations += total_observations_to_add #TODO refactor this process
        wrong_count += wrong_count_to_add

        print('Wrong Count: %s' % wrong_count)
        print('Total Tags: %s' % total_observations)
        print('Tagging Accuracy: %.2f%%' % ((1 - float (wrong_count) / total_observations)*100)) #TODO True accuracy measure may need to remove the added SOS tags


    def test_unknown_words(self, data):

        total_observations = 0
        wrong_count = 0

        #Split data into 10 sets and run algorithm over each
        for i in range(0,10): #TODO set back to 0,10 to iterate through all tests

            test_data = data[int(len(data) * .1 * i) : int(len(data) * (.1 * (i + 1)))]
            training_data = data[0 : int(len(data) * .1 * i)] + data[int(len(data) * .1 * (i + 1)) : int(len(data))] #TODO: implement unknown word handling
            total_observations_to_add, wrong_count_to_add = self.run_viterbi(test_data, training_data, i) #TODO: Improve this implementation
            total_observations += total_observations_to_add
            wrong_count += wrong_count_to_add

        print('Wrong Count: %s' % wrong_count)
        print('Total Tags: %s' % total_observations)
        print('Tagging Accuracy: %.2f%%' % ((1 - float (wrong_count) / total_observations)*100)) #TODO True accuracy measure may need to remove the added SOS tags


    def run_viterbi(self, test_data, training_data, pass_number):

        wrong_count = 0
        total_observations = 0

        #Removing tags in split test data until start of new sentence.
        #print test_data
        for j in test_data:
            if test_data[0] == ('SOS', 'SOS'):
                print('Found SOS tag, continuing with test data.')
                break
            else:
                print('Removing item: %s' % ' / '.join(test_data[0]))
                test_data.pop(0)

        stripped_test_data = [x[0] for x in test_data]

        print("Test data length: %s" % len(stripped_test_data))

        word_table = ProbabilityCounter().generate_word_pr_table(training_data, 1)
        cat_table = ProbabilityCounter().generate_cat_pr_table(training_data, 1)
        tag_list = list(cat_table.columns.values)

        #print cat_table.to_string()
        #print word_table.to_string()
        #print 'Tag List: %s' % tag_list

        print('Current WrongCount: %s' % wrong_count)
        print('Current Total Tags: %s' % total_observations)
        if total_observations > 0:
            print('Current Tagging Accuracy: %.2f%%' % ((1 - float (wrong_count) / total_observations)*100)) #TODO True accuracy measure may need to remove the added SOS tags

        print('Running Viterbi algorithm pass number: %d' % (pass_number +1) )
        opt = Viterbi().tagger_updated(stripped_test_data, tag_list, cat_table, word_table)

        true_tags = [x[1] for x in test_data]
        predicted_tags = [x[1] for x in opt]

        print(true_tags)
        print(predicted_tags)

        for j in range(0, len(predicted_tags)):
            if predicted_tags[j] != true_tags[j]:
                wrong_count += 1
        total_observations += len(predicted_tags)

        return total_observations, wrong_count


    # exports unique words and tags to CSV files for manual inspection
    def save_data_values(self, data):
        tag_filename = open('uniqueTags.txt', 'w')
        cat_data = [x[1] for x in data]
        cat_data = sorted(ProbabilityCounter().uniqify(cat_data))
        for elem in cat_data:
            tag_filename.write("%s\n" % elem)
        word_filename = open('uniqueWords.txt', 'w')
        #word_data = [x[0] for x in data]
        word_data = sorted(ProbabilityCounter().uniqify(data))
        for elem in word_data:
            word_filename.write("%s %s\n" % elem)


if __name__ == "__main__":
    Main()
