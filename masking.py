import spacy

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Load the small spaCy model once
loaded_spacy_model = spacy.load("en_core_web_sm")

# Reuse the loaded spaCy pipeline so Presidio doesn't load its default model again
class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_model):
        super().__init__()
        self.nlp = {"en": loaded_model}

nlp_engine = LoadedSpacyNlpEngine(loaded_model=loaded_spacy_model)

analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine,
    supported_languages=["en"]
)

anonymizer = AnonymizerEngine()

# TARGET_ENTITIES = ["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON"]

def mask_text(text):
    analyzer_results = analyzer.analyze(
        text=text,
        language="en",
        # entities=TARGET_ENTITIES
    )

    operators = {}
    for item in analyzer_results:
        operators[item.entity_type] = OperatorConfig(
            "replace",
            {"new_value": f"<{item.entity_type}>"}
        )

    result = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators=operators
    )

    return result.text


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
