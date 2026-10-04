def evaluate_results(results):
    correct = 0
    total = len(results)

    for result in results:
        if result["expected"].lower() == result["prediction"].lower():
            correct += 1

    accuracy = (correct / total) * 100

    print("\nEvaluation Results")
    print("------------------")
    print(f"Correct: {correct}")
    print(f"Total: {total}")
    print(f"Accuracy: {accuracy:.2f}%")

