# Reversible Natural Language Tokenizer
# Copyright (C) 2015  Ross Goodwin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can contact Ross Goodwin at ross.goodwin@gmail.com or address
# physical correspondence to:

# Ross Goodwin c/o ITP
# 721 Broadway
# 4th Floor
# New York, NY 10003


import string
import re


# USAGE:
# from tokenizer import Tokenize
# tokenized = Tokenize(string)

# METHODS: 
# tokenized.get_token_list()        Returns list of word tokens
# tokenized.untokenize()            Returns string of joined tokens with 

# ATTRIBUTES:
# tokenized.word_tokens       dictionaries  | Keys are token indices
# tokenized.punc_tokens                     | Values are tokens
# tokenized.space_tokens



class Tokenize(object):

    def __init__(self, text):
        # Punctuation
        self.punctuation = set(string.punctuation)

        # Whitespace
        self.whitespace = set(string.whitespace)

        # Letters and Digits
        self.alphanum = set(string.ascii_letters+string.digits)

        # Input Text
        self.text = text

        # Data dicts
        self.punc_tokens = {}
        self.space_tokens = {}
        self.word_tokens = {}

        # Set values of token list and dicts
        self._tokenize()


    def _tokenize(self):
        # THIS METHOD CALLED AUTOMATICALLY BY __init__

        # Extract tokens
        raw = re.findall(r"\b[a-zA-Z0-9']+\b|[^a-zA-Z0-9]+", self.text)

        # Populate data structures
        i = 0
        for token in raw:
            if not token:
                pass
            else:
                # self.tokens.append(token)
                # Order of if/elif statements is important...
                if set(token) & self.alphanum:
                    self.word_tokens[i] = token
                elif set(token) & self.punctuation:
                    self.punc_tokens[i] = token
                elif set(token) & self.whitespace:
                    self.space_tokens[i] = token
                else:
                    raise Exception("Unauthorized token at position %i" % i)
            i += 1


    def get_token_list(self, word_token_dict=False):
        if not word_token_dict:
            word_token_dict = self.word_tokens
        sorted_indices = sorted(word_token_dict)
        return [word_token_dict[i] for i in sorted_indices]


    def untokenize(self, word_token_dict=False, other_token_dicts=False):
        if not word_token_dict:
            word_token_dict = self.word_tokens
        if not other_token_dicts:
            other_token_dicts = [self.space_tokens, self.punc_tokens]

        dict_zero = other_token_dicts.pop()
        token_dict = dict(word_token_dict, **dict_zero)
        for d in other_token_dicts:
            token_dict.update(d)

        return ''.join(token_dict[i] for i in sorted(token_dict))
