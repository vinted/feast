"""
SETUP

* Install go
* Install protoc-gen-go:
    * go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
    * go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
* export PATH="$PATH:$(go env GOPATH)/bin"
* pip install -U pip
* pip install grpcio-tools pybindgen
* COMPILE_GO=true pip install -e ".[go,redis,gcp]"
* python test.py
"""
from feast import FeatureStore, RepoConfig

feast_client = FeatureStore(
    config=RepoConfig(
        project="marketplace_sandbox",
        registry="registry.db",
        provider="local",
        online_store={
            "type": "redis",
            "redis_type": "redis_cluster",
            "connection_string": "localhost:1234"
        },
        go_feature_retrieval=True,
    )
)

df = feast_client.get_online_features(features=["titanic_features_v1:Age", "titanic_features_v1:Pclass"], entity_rows=[{"PassengerId": 62}, {"PassengerId": 830}, {"PassengerId": 390}]).to_dict()
print(df)
