# import json
import os
from typing import Dict, List, Iterable

from category_class import Category

from logging_config import get_logger


_logger = get_logger(logger_name=__name__)


def log_too_many_elements_in_def(parsed_entry:  Dict[str, List[str]],
                                 definition_tag: str,
                                 ):
    try:
        defini = parsed_entry[definition_tag]
    except KeyError:
        pass
    else:
        if len(defini) > 1:
            _logger.debug("Too Many elements in Definition: " + str(defini))


def log_missing_language(parsed_entry:  Dict[str, List[str]],
                         first_language_tag: str,
                         second_language_tag: str,
                         ):
    try:
        parsed_entry[first_language_tag]
        parsed_entry[second_language_tag]
    except KeyError:
        _logger.debug('Missing Element in: ' + str(parsed_entry))


def get_parsed_entry(
  input_line: str,
  categories: Dict[str, str],
  prefix_n: int,  # number of letters identifying the element's category
  ) -> Dict[str, List[str]]:
    """Return a single glossary entry."""
    parsed_entry: dict = {}
    for element in input_line.strip().split("\t"):
        category = element[:prefix_n]

        if category not in parsed_entry.keys():
            elements_list = element[prefix_n:].split("|")
            parsed_entry[category] = [token.strip() for token in elements_list]
        else:
            _logger.debug(f"Repeated elements in entry: {parsed_entry}")

        # Make sure all tags (i.e. categories) are appropriate
        if category not in categories.values():
            _logger.debug(f"Invalid Category Found: {category}")

    # Defintions may contain extra ";", I want to find them
    log_too_many_elements_in_def(parsed_entry,
                                 Category.get_categories()['definition'],
                                 )
    # Both English and Russian terms must be in place
    log_missing_language(parsed_entry,
                         Category.get_categories()["english_term"],
                         Category.get_categories()["russian_term"],
                         )

    return parsed_entry


def count_max_elements(parsed_entry:  Dict[str, List[str]],
                       counts: Dict[str, int]) -> Dict[str, int]:
    """Return an updated counter of elements in the entry."""
    for key, val in parsed_entry.items():
        # if len(val) > counts[key]:
        #     counts[key] = len(val)
        counts[key] = len(val) if len(val) > counts[key] else counts[key]

    return counts


def pad_entry(parsed_entry: Dict[str, List[str]],
              counts: Dict[str, int]
              ) -> Dict[str, List[str]]:
    padded_entry = {}
    for tag, count in counts.items():
        try:
            num_elements = len(parsed_entry[tag])
        except KeyError:
            padded_entry[tag] = [""] * counts[tag]
        else:
            num_extra_elem = counts[tag] - num_elements
            padded_entry[tag] = parsed_entry[tag] + [""] * num_extra_elem

    return padded_entry


def stringify_entry(parsed_entry, headings, counts) -> str:
    """Return entry as a tab-delim string in correct order."""
    parsed_entry = pad_entry(parsed_entry, counts)
    entry_str = ""
    for tag, _ in headings:
        entry_str += ("\t".join(["{}"] * counts[tag]) + "\t").format(*parsed_entry[tag])

    return entry_str


if __name__ == "__main__":
    parsed_glossary: list = []
    counts: Dict[str, int] = {key: 0 for key in Category.get_categories().values()}
    path = os.path.join("data", "WHO-glossary-2009.txt")
    with open(path, "r", encoding="utf-8") as from_file:
        for line in from_file:
            parsed_entry = get_parsed_entry(
                line,
                Category.get_categories(),
                prefix_n=3,
                )
            parsed_glossary.append(parsed_entry)
            counts = count_max_elements(parsed_entry, counts)

    print(f"Number of elements in the glossary: {len(parsed_glossary)}")
    #  1503
    print(f"Count of max # of elements in entries: {counts}")
    #  {'ENG': 3, 'RUS': 4, 'SEE': 3, 'DEF': 1, 'CFR': 1, 'SYE': 4, 'SYR': 3}
    print(f"The 7th entry: {parsed_glossary[6]}")
    #  {'ENG': ['acceptable risk'], 'RUS': ['Приемлемый риск', ' приемлемая степень риска']}

    target = os.path.join("data", "who_glossary_2009.tsv")

    # Construct the heading for the data in the tsv-file contents
    full_heading = ""
    for tag, title in Category.get_headings():
        full_heading += ("\t".join(["{}"] * counts[tag]) + "\t").format(*[title] * counts[tag])

# YOU ARE A FUCKING IDIOT! NOT "path"!
    with open(target, "w", encoding="utf-8") as to_file:
        to_file.write(full_heading.strip())
        to_file.write('\n')
        for entry in parsed_glossary:
            to_file.write(stringify_entry(
                entry, headings=Category.get_headings(), counts=counts
                                          )
                          )
            to_file.write('\n')
