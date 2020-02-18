import config

class Parser:
    """This class parse a string to get
    a list of words ready to request an address"""

    @staticmethod
    def _split_in_words(sentence):
        """Takes a string as 'sentence'.
        Returns a list of lowered words"""
        assert isinstance(sentence, str)
        wrong_letters = []
        for letter in sentence:
            if letter not in wrong_letters+["-"] and not letter.isalnum():
                wrong_letters.append(letter)
        for letter in wrong_letters:
            sentence = sentence.replace(letter, " "+letter+" ")
        return sentence.lower().split()

    @staticmethod
    def _find_word(words_list, search_list, start=0):
        """Takes a list of words as 'words_list',
        a list of key words as 'search_list'
        and an int as start (default = 0).
        Searches if there is a keyword after the 'start' index in 'words_list'.
        Returns the index of the first founded keyword, or None if no match"""
        for index, word in enumerate(words_list[start:]):
            if word in search_list:
                return index+start
        return None


    def _parse_by_key_word(self, words_list):
        """Takes a list of words as 'words_list'.
        Search for a starting key word in 'words_list.
        Returns the words beetwen the starting key word and
        the ending key word, or an empty list if no match"""
        start = self._find_word(words_list, config.START_KEYWORDS)
        if start:
            stop = self._find_word(
                words_list, config.END_KEYWORDS, start=start)
            if not stop:
                stop = len(words_list)+1
            return words_list[start+1:stop]
        return []

    @staticmethod
    def _parse_by_filter(words_list):
        """Takes a list of words as 'words_list'.
        Returns the list without the words in a stopwords list"""
        parsed_list = []
        for word in words_list:
            if word.isalnum() and word not in config.STOPWORDS:
                parsed_list.append(word)
        return parsed_list

    def parse(self, sentence):
        """The main methods.
        Takes a string as 'sentence'.
        Calls a method to split 'sentence' in a word list.
        Tries to parses the list by key words.
        If this fails, parses the list by stopwords.
        Returns the parsed list"""
        words_list = self._split_in_words(sentence)
        parsed_list = self._parse_by_key_word(words_list)
        if not parsed_list:
            parsed_list = self._parse_by_filter(words_list)
        return parsed_list
