"""This module contains some tests."""


from main import (
    get_parsed_entry,
    pad_entry,
    stringify_entry,
    )
from category_class import Category


def test_get_parsed_entry():
    orig = "ENG Accelerated | Disease Control	RUS Активизация борьбы с болезнями	DEF Стратегии для ускорения темпов борьбы с определенными инфекционными болезнями."
    expected = {"ENG": ["Accelerated", "Disease Control"],
                "RUS": ["Активизация борьбы с болезнями"],
                "DEF": ["Стратегии для ускорения темпов борьбы с определенными инфекционными болезнями."],
                }
    parsed_entry = get_parsed_entry(
        orig,
        Category.get_categories(),
        prefix_n=3,
        )
    assert parsed_entry == expected

    orig = "ENG antibody-mediated immunity	SYE humoral immunity	RUS Иммунитет, обусловленный антителами	SYR Гуморальный иммунитет"
    expected = {"ENG": ["antibody-mediated immunity"],
                "RUS": ["Иммунитет, обусловленный антителами"],
                "SYE": ["humoral immunity"],
                "SYR": ["Гуморальный иммунитет"],
                }
    parsed_entry = get_parsed_entry(
        orig,
        Category.get_categories(),
        prefix_n=3,
        )
    assert parsed_entry == expected


def test_pad_entry_function():
    entry = {'ENG': ['acceptable risk'],
             'RUS': ['Приемлемый риск', 'приемлемая степень риска']
             }
    result = pad_entry(parsed_entry=entry,
                       counts={"ENG": 3, "RUS": 4, "DEF": 1}
                       )
    expected = {"ENG": ["acceptable risk", "", ""],
                "RUS": ["Приемлемый риск", "приемлемая степень риска", "", ""],
                "DEF": [""],
                }
    assert result == expected

    result = pad_entry(parsed_entry=entry,
                       counts={"ENG": 3, "RUS": 4, "DEF": 2}
                       )
    expected = {"ENG": ["acceptable risk", "", ""],
                "RUS": ["Приемлемый риск", "приемлемая степень риска", "", ""],
                "DEF": ["", ""],
                }
    assert result == expected


def test_stringify_entry():
    entry = {"ENG": ["a", "b"], "RUS": ["а", "б"]}
    result = stringify_entry(parsed_entry=entry,
                             headings=(("ENG", ""), ("RUS", ""), ("DEF", "")),
                             counts={"ENG": 3, "RUS": 3, "DEF": 1}
                             )
    expected = "a\tb\t\tа\tб\t\t\t"
    assert result == expected
