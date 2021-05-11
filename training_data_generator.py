from services.search_service import Index, index
from typing import List, Set
from random import sample
from random import randint, random
import string
import json
import asyncio
from engines.vector import VectorEngine

def generate_data(index: Index, terms: Set[str], docs: int):
    def generate_query() -> List[str]:
        random_strings = set(
            "".join(sample(string.ascii_letters, randint(4, 10))) for _ in range(100)
        )
        return sample(terms.union(random_strings), randint(1, 10))

    for epochs in range(1000):
        query = generate_query()
        print(f"Generated {query} for training")
        query_vector = VectorEngine.compute_query_vector(index, query)
        similarity = []
        for doc in range(docs):
            doc_vector = VectorEngine.compute_doc_vector(index, doc)
            s = VectorEngine.compute_sim(query_vector, doc_vector)
            similarity.append(s)

        correct_similarity = [0.0] * docs

        for i in range(docs):
            if similarity[i] > 0:
                correct_similarity[i] = 0 if random() > 1 / 2 else random()

        yield {
            "query": query,
            "query_vector": query_vector,
            "computed_data": similarity,
            "correct_data": correct_similarity,
        }


async def main():
    await Index.initialize(index)

    json_data = [
        data
        for data in generate_data(
            index, set(index.system_terms.keys()), index.total_documents
        )
    ]

    with open("training.json","w") as file:
        file.write(json.dumps(json_data, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
