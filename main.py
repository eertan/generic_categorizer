from generic_classifier import GenericCategorizer
import dspy

lm = dspy.LM("gemini/gemini-3-pro-preview")
dspy.configure(lm=lm)

def main():

    # topic = "Inbound Sales"

    # categories = {
    #     "Pricing": "Cost and payment inquiries.",
    #     "Technical": "Product specs and compatibility."
    # }

    # subcategories = {
    #     "Enterprise": "Corporate plans.",
    #     "Individual": "Personal plans."
    # }
    topic = "Law Enforcement Knowledge Management System"

    categories = {
        "Data-Related": "Questions that require direct access to or the knowledge of the data within the system. These questions focus on the content and structure of the data itself.",
        "System-Related": "Questions related to system's functionality such as features, architecture,design, etc.. Information can be found in documentation, not the data itself.",
        "Feedback/Complaints": "Questions that are either not answerable by the system or about user feedback and complaints"
    }

    subcategories = {
        "Documentation-Related": "Questions that can be answered by referring to the system documentation like user manuals or help sections. Only applies for System-Related category, otherwise None",
        "Schema-Related": "Questions related to the structure of the knowledge graph or the graph data schema. Only applies for System-Related category, otherwise None",
    }

    categorizer = GenericCategorizer(topic, categories, subcategories)
    questions = ["Is it possible to export data from system into CSV file?",
        "How do I use the system to asess the risk level associated with a suspect or location?",
        "What permissions do I need to access restricted data?",
        "Why isn't the system responding to my queries?",
        "What type of data visualizations can the system generate?"
    ]
    for q in questions:
        pred = categorizer(q)

        print(pred)

if __name__ == "__main__":
    main()
