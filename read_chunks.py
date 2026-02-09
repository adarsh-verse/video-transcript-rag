import requests
import pandas as pd
import json
import os
import joblib

OUTPUT_DIR = "outputs"
EMBEDDING_FILE = "embeddings.joblib"


def create_embedding(text):
    r = requests.post("http://localhost:11434/api/embeddings",
        json={
            "model": "bge-m3",
            "prompt": text
        }
    )
    return r.json()["embedding"]


df = pd.DataFrame(
    columns=[
        "video_number",
        "title",
        "start",
        "end",
        "text",
        "chunk_id",
        "embedding"
    ]
)


if __name__ == "__main__":

    for file_name in os.listdir(OUTPUT_DIR):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(OUTPUT_DIR, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for index, chunk in enumerate(data["chunks"]):
            text = chunk["text"]
            print(f"Creating embedding for chunk {index}")

            embedding = create_embedding(text)

            df.loc[len(df)] = [
                chunk["video_number"],
                chunk["title"],
                chunk["start"],
                chunk["end"],
                text,
                f"{chunk['video_number']}_{file_name}_{index}",
                embedding
            ]

    joblib.dump(df, EMBEDDING_FILE)

    print(f"Total chunks: {len(df)}")
    print("File created successfully")
