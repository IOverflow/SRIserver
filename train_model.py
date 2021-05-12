from services.search_service import Index, index
from engines.ranking.nn_model import ranker, FeedForwardRankingNNModel
import asyncio

async def main():
    await Index.initialize(index)

    # Build the NN model for tunning retrieved documents quality
    vocabulary = len(index.system_terms.keys())
    ranker.initialize(vocabulary=vocabulary, docs=index.total_documents)

    # Train the model against known queries and relevant documents
    inputs, targets = FeedForwardRankingNNModel.generate_data_from_json()
    ranker.train(inputs, targets)

    score = ranker.model.evaluate(inputs, targets)
    print(score)
    print("%s: %.2f%%" % (ranker.model.metrics_names[1], score[1]*100))

    with open("model.json", "w") as json_file:
        model_bytecode = ranker.model.to_json()
        json_file.write(model_bytecode)

    # save weights
    ranker.model.save_weights("model.h5")

if __name__ == '__main__':
    asyncio.run(main())