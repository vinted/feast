from datetime import datetime
from typing import Dict, List

import pandas as pd

from feast import FeatureStore, RepoConfig

ENTITIES_DF = pd.read_csv("pasanger_id_400.csv")
ENTITIES_1 = ENTITIES_DF[:1].to_dict(orient="records")
ENTITIES_50 = ENTITIES_DF[:50].to_dict(orient="records")
ENTITIES_100 = ENTITIES_DF[:100].to_dict(orient="records")
ENTITIES_200 = ENTITIES_DF[:200].to_dict(orient="records")
ENTITIES_400 = ENTITIES_DF[:400].to_dict(orient="records")

# FEATURES = [
#     "titanic_features_v1:Sex",
#     "titanic_features_v1:Age",
#     "titanic_features_v1:SibSp",
#     "titanic_features_v1:Parch",
#     "titanic_features_v1:Fare",
#     "titanic_features_v1:Cabin",
#     "titanic_features_v1:Embarked",
# ]

FEATURES = [
    "titanic_features_v1:Sex",
    "titanic_features_v1:SibSp",
    "titanic_features_v1:Parch",
    "titanic_features_v1:Fare",
    "titanic_features_v1:Embarked",
]

def measure_online_features(
    feature_store: FeatureStore,
    features: List[str],
    entity_rows: List[Dict],
) -> float:
    start_time = datetime.now()
    feature_store.get_online_features(
        features=features, entity_rows=entity_rows
    )
    return (datetime.now() - start_time).total_seconds() * 1000


def calculate_mesurements(mesurements: List[float]) -> None:
    m_series = pd.Series(mesurements)
    m_describe = m_series.describe()
    print(
        "measurements: "
        f"{', '.join(str(round(s, 2)) for s in mesurements[:10])} ..."
    )
    print(f"mean: {m_describe['mean']:.2f}ms")
    print(f"min: {m_describe['min']:.2f}ms")
    print(f"50%: {m_describe['50%']:.2f}ms")
    print(f"99%: {m_series.quantile(.99):.2f}ms")
    print(f"max: {m_describe['max']:.2f}ms")


def run_test(
    feature_store: FeatureStore,
    features: List[str],
    entity_rows: List[Dict],
    iteration_nr: int,
    test_name: str,
) -> None:
    total = []

    for _ in range(iteration_nr):
        total.append(
            measure_online_features(feature_store, features, entity_rows)
        )

    print("#" * 60)
    print(f"{test_name}")
    print(f"Iterations: {iteration_nr}")
    print(
        "#" * 10,
        "Total",
        "#" * 10,
    )
    calculate_mesurements(total)
    print("#" * 60)


if __name__ == "__main__":
    fs = FeatureStore(
        config=RepoConfig(
            project="marketplace_sandbox",
            registry="registry.db",
            provider="local",
            online_store={
                "type": "redis",
                "redis_type": "redis_cluster",
                "connection_string": "vmip-feast-experiment.redis-cluster.service.consul:6514,vmip-feast-experiment.redis-cluster.service.consul:6515,vmip-feast-experiment.redis-cluster.service.consul:6516",
            },
            go_feature_retrieval=True,
        )
    )

    run_test(
        feature_store=fs,
        features=FEATURES,
        entity_rows=ENTITIES_1,
        iteration_nr=100,
        test_name="Titanic 1 entity",
    )

    run_test(
        feature_store=fs,
        features=FEATURES,
        entity_rows=ENTITIES_50,
        iteration_nr=100,
        test_name="Titanic 50 entities",
    )

    run_test(
        feature_store=fs,
        features=FEATURES,
        entity_rows=ENTITIES_100,
        iteration_nr=100,
        test_name="Titanic 100 entities",
    )

    run_test(
        feature_store=fs,
        features=FEATURES,
        entity_rows=ENTITIES_200,
        iteration_nr=100,
        test_name="Titanic 200 entities",
    )

    run_test(
        feature_store=fs,
        features=FEATURES,
        entity_rows=ENTITIES_400,
        iteration_nr=100,
        test_name="Titanic 400 entities",
    )
