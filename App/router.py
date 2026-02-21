from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

Route.__hash__ = lambda self: hash(id(self))


def route_eq(self, other):
    if isinstance(other, str):
        return self.name == other
    if hasattr(other, "name"):
        return self.name == other.name
    return False


Route.__eq__ = route_eq

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq_utterances = [
    "What is the return policy of the products?",
    "Do I get discount with the HDFC credit card?",
    "How can I track my order?",
    "What payment methods are accepted?",
    "How long does it take to process a refund?",
]

sql_utterances = [
    "I want to buy nike shoes that have 50% discount.",
    "Are there any shoes under Rs. 3000?",
    "Do you have formal shoes in size 9?",
    "Are there any Puma shoes on sale?",
    "What is the price of puma running shoes?",
]


all_routes = []

for text in faq_utterances:
    all_routes.append(Route(name="faq", utterances=[text]))

for text in sql_utterances:
    all_routes.append(Route(name="sql", utterances=[text]))

# 4. Initialize Router
router = SemanticRouter(
    encoder=encoder,
    routes=all_routes
)

try:
    index_utterances = []
    index_routes = []

    for route in all_routes:
        index_utterances.append(route.utterances[0])
        index_routes.append(route)

    embeddings = encoder(index_utterances)

    router.index.add(
        embeddings=embeddings,
        routes=index_routes,
        utterances=index_utterances
    )
    print("Index built successfully.")

except Exception as e:
    print(f"Index build failed: {e}")

if __name__ == "__main__":
    print("-" * 30)

    resp1 = router("Do I get discount with the HDFC credit card?")
    print(f"Query 1: {resp1.name}")

    resp2 = router("Pink Puma shoes in price range 5000 to 1000")
    print(f"Query 2: {resp2.name}")