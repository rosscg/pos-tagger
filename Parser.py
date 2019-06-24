import os
import re

regex = re.compile('([^\n ]+)\/([^\n ]+)')
number_ex = re.compile('^[0-9]+(([\.,][0-9]+)+)?$') #TODO dollar sign here added to anchor to end of string, may need to make another regex to match other number phrases. May need to adjust to account for fractions (eg. 1\/2)


# TODO to lowercase, clean conjunctions, other specials, change all numbers to a tag, add start of sentence tags


class Parser:

    def __init__(self):
        self.sentence_list = []

    def opendirs(self, text_file_path):
        # Walk through the directory of input files
        file_contents = ''
        for root, dirs, files in os.walk(text_file_path, topdown=False):
            for name in files: #TODO may need to add an exclusion for hidden files beginning with . (eg. .DS_Store)
                # print(os.path.join(root, name))
                f = open(os.path.join(root, name))
                # Add file to string - TODO: care that file append does not merge two words
                file_contents += f.read()
        return file_contents

    def parse(self, raw_text):
        parsed_text = [('SOS', 'SOS')] # Placing Start of Sentence tag at beginning of list
        for match in re.finditer(regex, raw_text):

            #replace numbers with numbertag
            if number_ex.match(match.group(1)):
                print('Number removed: %s' % match.group(1))
                parsed_text.append(('tag_number', 'CD'))
            else:
                parsed_text.append((match.group(1).lower(), match.group(2)))

            if (match.group(1).lower(), match.group(2)) == ('.', '.'):  # Adding Start of Sentence tags after periods.
                parsed_text.append(('SOS', 'SOS'))

        # Remove SOS tag which has been placed at end of list if it ends in a period.
        if parsed_text[len(parsed_text)-1] == ('SOS', 'SOS'):
            parsed_text.pop()
            print('Removing SOS tag placed at end of string..')

        return parsed_text

    def save_file(self):
        filename = open('tempOutputData.txt', 'w')
        for elem in self.sentence_list:
            filename.write("%s, %s\n" % elem)

    def parse_from_path(self, path):
        self.sentence_list = self.parse(self.opendirs(path))
        return self.sentence_list

    def trim_data(self, data): #TODO As yet unused
        number_ex = '[0-9]+(([\.\,][0-9]+)+)?'
        ordinal_ex = '[0-9]+(([\.\,][0-9]+)+)?(st|nd|rd|th|)'
        print(data)
        return data

    def remove_new_words(self, training_data, test_data):
        print('to be completed')


if __name__ == "__main__":
    m = Parser().parse_from_path('text/02')
    for elem in m:
        print ("%s %s\n" % elem)