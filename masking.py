import spacy

from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern,
    RecognizerRegistry
)
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# -----------------------------
# 1) Loading the spaCy small model once, since large onces not be able to get used by render. . . . 
# -----------------------------
loaded_spacy_model = spacy.load("en_core_web_sm")

class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_model):
        super().__init__()
        self.nlp = {"en": loaded_model}

nlp_engine = LoadedSpacyNlpEngine(loaded_model=loaded_spacy_model)

# -----------------------------
# 2) Helper to create regex recognizers easily
# -----------------------------
def make_regex_recognizer(entity_name, regex, score=0.5, context=None):
    pattern = Pattern(
        name=f"{entity_name.lower()}_pattern",
        regex=regex,
        score=score
    )
    return PatternRecognizer(
        supported_entity=entity_name,
        patterns=[pattern],
        context=context or []
    )

# -----------------------------
# 3) Your custom recognizers
# -----------------------------
customs = [
    make_regex_recognizer(
        "ACCOUNT_NUMBER",
        r"\b\d{10,18}\b",
        0.6,
        ["account", "acct", "bank", "account number"]
    ),
    make_regex_recognizer(
        "PIN_NUMBER",
        r"\b\d{4,6}\b",
        0.4,
        ["pin", "otp", "passcode", "verification code"]
    ),
    make_regex_recognizer(
        "PASSWORD",
        r"(?i)(password\s*(is|=|:)\s*[^\s,;]+)",
        0.8,
        ["password", "pwd", "secret"]
    )
]
# -----------------------------
# 4) Build registry:
#    default Presidio + your customs
# -----------------------------
registry = RecognizerRegistry()
registry.load_predefined_recognizers()

for recognizer in customs:
    registry.add_recognizer(recognizer)


analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine,
    registry=registry,
    supported_languages=["en"]
)

anonymizer = AnonymizerEngine()

def mask_text(text):
    analyzer_results = analyzer.analyze(
        text=text,
        language="en"
    )

    operators = {}
    for item in analyzer_results:
        # original_value = text[item.start:item.end]
        original_value = item.entity_type
        operators[item.entity_type] = OperatorConfig(
            "replace",
            {"new_value": "*" * len(original_value)}
        )

    result = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators=operators
    )
    
    return result.text



# import spacy

# from presidio_analyzer import AnalyzerEngine
# from presidio_analyzer.nlp_engine import SpacyNlpEngine
# from presidio_anonymizer import AnonymizerEngine
# from presidio_anonymizer.entities import OperatorConfig

# # Load the small spaCy model once
# loaded_spacy_model = spacy.load("en_core_web_sm")

# # Reuse the loaded spaCy pipeline so Presidio doesn't load its default model again
# class LoadedSpacyNlpEngine(SpacyNlpEngine):
#     def __init__(self, loaded_model):
#         super().__init__()
#         self.nlp = {"en": loaded_model}

# nlp_engine = LoadedSpacyNlpEngine(loaded_model=loaded_spacy_model)

# analyzer = AnalyzerEngine(
#     nlp_engine=nlp_engine,
#     supported_languages=["en"]
# )

# anonymizer = AnonymizerEngine()

# # TARGET_ENTITIES = ["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON"]

# def mask_text(text):
#     analyzer_results = analyzer.analyze(
#         text=text,
#         language="en",
#         # entities=TARGET_ENTITIES
#     )

#     operators = {}
#     for item in analyzer_results:
#         len_entity=len(item.entity_type)
#         operators[item.entity_type] = OperatorConfig(
#             "replace",
#             # {"new_value": f"<{item.entity_type}>"}
#             {"new_value": "*"*len_entity}
            
#         )

#     result = anonymizer.anonymize(
#         text=text,
#         analyzer_results=analyzer_results,
#         operators=operators
#     )

#     return result.text


# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine
# from presidio_anonymizer.entities import OperatorConfig

# analyzer = AnalyzerEngine()
# anonymizer = AnonymizerEngine()

# def mask_text(text):
#     analyzer_results = analyzer.analyze(
#         text=text,
#         language="en"
#     )

#     operators = {}
#     for item in analyzer_results:
#         operators[item.entity_type] = OperatorConfig(
#             "replace",
#             {"new_value": f"<{item.entity_type}>"}
#         )

#     result = anonymizer.anonymize(
#         text=text,
#         analyzer_results=analyzer_results,
#         operators=operators
#     )

#     return result.text

# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine
# from presidio_anonymizer.entities import OperatorConfig

# def mask_text(text):
#     analyzer = AnalyzerEngine()
#     analyzer_results = analyzer.analyze(
#         text=text,
#         language="en"
#     )

#     anonymizer = AnonymizerEngine()

#     operators = {}
#     for item in analyzer_results:
#         operators[item.entity_type] = OperatorConfig(
#             "replace",
#             {"new_value": f"<{item.entity_type}>"}
#         )

#     result = anonymizer.anonymize(
#         text=text,
#         analyzer_results=analyzer_results,
#         operators=operators
#     )

#     return result.text


# if __name__ == "__main__":
#     sample = "Hi, my name is Aryasen Gupta. My phone number is 212-555-5555 and email is aryasen@example.com"
#     print(mask_text(sample))
