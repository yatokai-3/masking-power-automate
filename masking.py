from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

def mask_text(text):
    analyzer = AnalyzerEngine()
    analyzer_results = analyzer.analyze(
        text=text,
        language="en"
    )

    anonymizer = AnonymizerEngine()

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


# if __name__ == "__main__":
#     sample = "Hi, my name is Aryasen Gupta. My phone number is 212-555-5555 and email is aryasen@example.com"
#     print(mask_text(sample))
