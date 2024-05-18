import random
import string
import json


def generate_dataset():
    characters = string.ascii_letters + string.digits
    dataset = []

    for length in range(5, 6):  # Adjust the range to generate more strings if needed
        for _ in range(50):  # Number of samples per length
            sample = ''.join(random.choices(characters, k=length))
            dataset.append(sample)
    return dataset


def main():
    dataset = generate_dataset()
    with open("dataset.json", "w") as f:
        json.dump(dataset, f)


if __name__ == "__main__":
    main()
