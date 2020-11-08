"""This module contains categories of elements in the WHO glossary entries."""


class Category:
    """This class provides categories to search for in the txt glossary."""

    @classmethod
    def get_categories(cls):
        """Return {full_tag: short_tag} pairs."""
        return {
                "english_term": "ENG",
                "russian_term": "RUS",
                "see_also": "SEE",
                "definition": "DEF",
                "compare": "CFR",
                "synonyms_english": "SYE",
                "synonyms_russian": "SYR",
                }

    @classmethod
    def get_headings(cls):
        """Return (short_tag, human_title) pairs."""
        return (
                (cls.get_categories()["english_term"], "English"),
                (cls.get_categories()["synonyms_english"], "Synonym"),
                (cls.get_categories()["russian_term"], "Russian"),
                (cls.get_categories()["synonyms_russian"], "Synonym"),
                (cls.get_categories()["definition"], "Definition"),
                (cls.get_categories()["compare"], "Compare"),
                (cls.get_categories()["see_also"], "See_also"),
                )
