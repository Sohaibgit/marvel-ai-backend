
from app.tools.multiple_choice_quiz_generator.core import executor

quiz = executor(
    topic="Science Terms Vocabulary",
    n_questions=10,
    file_url="attached_assets/Science_Glossary.pdf",
    file_type="pdf",
    lang="en"
)

for i, question in enumerate(quiz, 1):
    print(f"\nQuestion {i}:")
    print(question['question'])
    print("\nChoices:")
    for key, value in question['choices'].items():
        print(f"{key}: {value}")
    print(f"\nCorrect Answer: {question['answer']}")
    print(f"Explanation: {question['explanation']}")
