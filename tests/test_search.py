from typing import Dict, List, Union
from fastapi.testclient import TestClient
from ..app import app
import numpy as np
import json
from colorama import Fore
from alive_progress import alive_bar


def test_get_vocabulary():
    with TestClient(app) as testClient:
        response = testClient.get("/search/vocabulary")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert all(
            term
            not in [
                "in",
                "and",
                "or",
                "an",
                "a",
                "the",
                "that",
                "what",
            ]
            for term in response.json()
        )


def test_precision_raw_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []
        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved: int = len(response.json()["diseases"])

                def is_relevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] > 0

                relevants: int = len(
                    list(filter(is_relevant, response.json()["diseases"]))
                )

                precision = relevants / retrieved if retrieved > 0 else 1.0

                assert 0 <= precision <= 1
                precisions.append(precision)
                bar()

            raw_search_precision = np.mean(np.array(precisions))
            print(
                f"\n{Fore.GREEN}PRECISION IN RAW SEARCH: {raw_search_precision}{Fore.RESET}"
            )


def test_precision_enhanced_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []
        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search/ranked", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved: int = len(response.json()["diseases"])

                def is_relevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] > 0

                relevants: int = len(
                    list(filter(is_relevant, response.json()["diseases"]))
                )

                precision = relevants / retrieved if retrieved > 0 else 1.0

                assert 0 <= precision <= 1
                precisions.append(precision)

                bar()

            raw_search_precision = np.mean(np.array(precisions))
            print(
                f"\n{Fore.GREEN}PRECISION IN ENHANCED SEARCH: {raw_search_precision}{Fore.RESET}"
            )


def test_recovery_raw_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []

        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved_docs: List[int] = list(
                    x["id"] for x in response.json()["diseases"]
                )

                def is_relevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] > 0

                def is_relevant_and_not_retrieved(doc):
                    return target[doc] > 0 and not doc in retrieved_docs

                relevants: int = len(
                    list(filter(is_relevant, response.json()["diseases"]))
                )
                non_retrieved_relevants: int = len(
                    list(
                        filter(
                            is_relevant_and_not_retrieved,
                            range(len(target)),
                        )
                    )
                )

                try:
                    recovery = relevants / (relevants + non_retrieved_relevants)
                except:
                    recovery = 1

                assert 0 <= recovery <= 1
                precisions.append(recovery)

                bar()

            raw_search_precision = np.mean(np.array(precisions))
            print(
                f"\n{Fore.GREEN}RECOVERY IN RAW SEARCH: {raw_search_precision}{Fore.RESET}"
            )


def test_recovery_enhanced_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []

        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search/ranked", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved_docs: List[int] = list(
                    x["id"] for x in response.json()["diseases"]
                )

                def is_relevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] > 0

                def is_relevant_and_not_retrieved(doc):
                    return target[doc] > 0 and not doc in retrieved_docs

                relevants: int = len(
                    list(filter(is_relevant, response.json()["diseases"]))
                )
                non_retrieved_relevants: int = len(
                    list(
                        filter(
                            is_relevant_and_not_retrieved,
                            range(len(target)),
                        )
                    )
                )

                try:
                    recovery = relevants / (relevants + non_retrieved_relevants)
                except:
                    recovery = 1

                assert 0 <= recovery <= 1
                precisions.append(recovery)

                bar()

            raw_search_precision = np.mean(np.array(precisions))
            print(
                f"\n{Fore.GREEN}RECOVERY IN ENHANCED SEARCH: {raw_search_precision}{Fore.RESET}"
            )


def test_fallout_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []

        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved_docs: List[int] = list(
                    x["id"] for x in response.json()["diseases"]
                )

                def is_irrelevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] == 0

                def is_irrelevant_and_not_retrieved(doc):
                    return target[doc] == 0 and not doc in retrieved_docs

                irrelevants: int = len(list(filter(is_irrelevant, response.json()["diseases"])))

                n_irrelevants: int = len(
                    list(
                        filter(
                            is_irrelevant_and_not_retrieved,
                            range(len(target)),
                        )
                    )
                )

                fallout = irrelevants / n_irrelevants

                precisions.append(fallout)

                bar()

            fallout = np.mean(np.array(precisions))
            print(f"\n{Fore.GREEN}FALLOUT IN RAW SEARCH: {fallout}{Fore.RESET}")


def test_fallout_enhanced_search():
    data: List[Dict[str, Union[List[str], List[float]]]] = []

    with open("training.json", "r") as json_file:
        data = json.loads(json_file.read())

    queries: List[List[str]] = list(x["query"] for x in data)
    targets: List[List[float]] = list(x["correct_data"] for x in data)

    with TestClient(app) as test_client:
        precisions: List[float] = []

        with alive_bar(len(targets), spinner="pulse") as bar:
            for query, target in zip(queries, targets):
                q = " ".join(query)
                response = test_client.get("/search/ranked", params={"query": q})

                assert response.status_code == 200

                # Report precision
                retrieved_docs: List[int] = list(
                    x["id"] for x in response.json()["diseases"]
                )

                def is_irrelevant(doc) -> bool:
                    index: int = doc["id"] - 1
                    return target[index] == 0

                def is_irrelevant_and_not_retrieved(doc):
                    return target[doc] == 0 and not doc in retrieved_docs

                irrelevants: int = len(list(filter(is_irrelevant, response.json()["diseases"])))

                n_irrelevants: int = len(
                    list(
                        filter(
                            is_irrelevant_and_not_retrieved,
                            range(len(target)),
                        )
                    )
                )

                fallout = irrelevants / n_irrelevants

                precisions.append(fallout)

                bar()

            fallout = np.mean(np.array(precisions))
            print(f"\n{Fore.GREEN}FALLOUT IN ENHANCED SEARCH: {fallout}{Fore.RESET}")