# sample000
## 概要
他のサンプルコードで使用する共通リソースをCloudFormationで作成します。  

## 作成されるリソース
- S3 Bucket
- VPC
- IAM Role (IAM実行ロール)

##  CloudFormationのデプロイコマンド例
```
$ cd sample000/

$ aws cloudformation package \
  --template-file ./template/template.yml \
  --s3-bucket my-work-bucket \
  --output-template-file ./template/template.packaged.yml

$ aws cloudformation deploy \
  --template-file ./template/template.packaged.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --stack-name sample-common-resource
```