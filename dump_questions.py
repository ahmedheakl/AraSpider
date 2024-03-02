"""Dump and process translated questions to the json Spider dataset"""

import json
import re

import pandas as pd

TRANSLATION_FILE = "data/translated_questions.csv"
SPIDER_FILE = "data/train_spider.json"


def preprocess_question(question: str) -> str:
    """Preprocess the question."""

    question = re.sub(re.compile(r"\[Translation]\s*"), "", question)
    question = re.sub(re.compile(r"\[Question]\s*"), "", question)
    question = re.sub(re.compile(r"\""), "", question)
    question = re.sub(re.compile(r"^[><]"), "", question)
    question = re.sub(re.compile(r"سؤال\s*:"), "", question)
    question = question.strip()
    return question


def main():
    """Main entry point for the script."""
    df = pd.read_csv(TRANSLATION_FILE)
    df = df[["translation"]]
    df = df.dropna()

    with open(SPIDER_FILE, "r") as f:
        spider = json.load(f)

    for i, row in df.iterrows():

        spider[i]["arabic_question"] = preprocess_question(row["translation"])

    with open(SPIDER_FILE, "w") as f:
        json.dump(spider, f, indent=4, ensure_ascii=False)

    print("Done!")


if __name__ == "__main__":
    main()
