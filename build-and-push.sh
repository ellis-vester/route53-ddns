$AWS_ACCOUNT_ID
$AWS_REGION

docker build -t route53-ddns .
docker tag route53-ddns $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/route53-ddns
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/route53-ddns