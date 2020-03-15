# #012. CloudFomrtionでMySQL互換のAuroraをつくる
## 概要
CloudFormationを使ってMySQL5.7互換のAuroraを作成します。

## 作成されるリソース
- RDS
  - DBCluster
  - DBInstance
  - DBSubnetGroup
- SecurityGroup

## CloudFormationテンプレートの作成コマンド例
```
$ python3 -m sample012.rds sample012
```

##  CloudFormationのデプロイコマンド例
```
aws cloudformation deploy \
  --template-file ./aurora.yml \
  --stack-name aurora-sample \
  --parameter-overrides DBMasterUserName=${DB_USER_NAME} \
    DBMasterUserPassword=${DB_USER_PASSWORD}
```