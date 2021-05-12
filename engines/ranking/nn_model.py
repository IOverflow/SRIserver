from typing import Any, Dict, List, Tuple
import tensorflow.keras as keras
import numpy as np
import json


class FeedForwardRankingNNModel:
    def __init__(self) -> None:
        self.model = None

    @staticmethod
    def generate_data_from_json(file="training.json") -> Tuple[np.ndarray, np.ndarray]:
        x = []
        y = []
        with open(file, "r") as _file:
            data: List[Dict[str, Any]] = json.loads(_file.read())
            for train_set in data:
                docs = np.array(train_set["computed_data"], dtype=np.float)
                query = np.array(list(train_set["query_vector"].values()), dtype=np.float)
                x.append(np.concatenate((docs, query)))
                y.append(np.array(train_set["correct_data"]))
        return np.array(x), np.array(y)

    def initialize(self, vocabulary: int, docs: int) -> None:
        m = vocabulary
        # Use the keras functional API to build the desired
        # network architecture

        # Input layer consist of a vector of n + m components
        # where n is our total of documents and m is the total of
        # terms in the vocabulary
        input_tensor = keras.Input((docs + m,))

        # Divide the input vector in 2 groups to connect the network
        # Get the neurons that reprensent the docs
        d_layer = keras.layers.Lambda(lambda t: t[:, :docs], output_shape=(docs,))(
            input_tensor
        )
        q_layer = keras.layers.Lambda(lambda t: t[:, docs:], output_shape=(m,))(
            input_tensor
        )

        # Connect each term neuron to the component in the query vector and then
        # merge each neuron into a single connected layer
        hidden_layer = []

        for i in range(m):
            projection_layer = keras.layers.Lambda(lambda t: t[:, i : (i + 1)])(q_layer)
            tensor = keras.layers.Concatenate()([d_layer, projection_layer])
            perceptron = keras.layers.Dense(1)(tensor)
            hidden_layer.append(perceptron)

        terms_layer = keras.layers.Concatenate()(hidden_layer)

        # Fully connect the docs vector with the terms layer
        output_layer = keras.layers.Dense(docs)(terms_layer)

        self.model = keras.models.Model(inputs=input_tensor, outputs=output_layer)

    def train(self, input_data: np.ndarray, target_data: np.ndarray) -> None:
        # Prepare the model for trainig
        self.model.compile(optimizer="sgd", loss=keras.losses.MeanSquaredError())

        # train it
        self.model.fit(
            input_data,
            target_data,
            verbose=1,
            validation_split=0.1,  # validate against 10% of data
            epochs=100,
        )

    def compute(
        self, activated_docs: np.ndarray, query_vector: np.ndarray
    ) -> np.ndarray:
        input_vector = np.concatenate((activated_docs, query_vector))
        input_vector = input_vector.reshape(1, input_vector.size)
        result = self.model.predict(input_vector)
        assert isinstance(result, np.ndarray)
        return result

    def __call__(self):
        return self


ranker = FeedForwardRankingNNModel()
