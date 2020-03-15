# #016. CloudFomrtionでFargate起動タイプのECSをつくる
## 概要
CloudFormationを使ってFargate起動タイプのECSを作成します。  
コンテナイメージはECRを使用せず、公式のnginxのイメージを使用します。  
AutoScalingは設定しません。

## 作成されるリソース
- SecurityGroup
  - ALB用のSecurityGroup
  - ECS用のSecurityGroup

- Application Load Balancer
  - LoadBalancer
  - Listener
  - TargetGroup

- ECS
  - Cluster
  - Service
  - TaskDefinition

## CloudFormationテンプレートの作成コマンド例
```
$ python3 -m sample016.ecs
```

## CloudFormationのデプロイコマンド例
```
# SecurityGroupをデプロイ
$ aws cloudformation deploy \
  --template-file ./sg.yml \
  --stack-name fargate-sample-sg

# ALBをデプロイ
$ aws cloudformation deploy \
  --template-file ./alb.yml \
  --stack-name fargate-sample-alb

# ECSをデプロイ
$ aws cloudformation deploy \
  --template-file ./ecs.yml \
  --stack-name fargate-sample
```