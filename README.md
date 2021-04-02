# route53-ddns

Docker container that performs DDNS synchronization against a DNS record registered with Amazon Route53.

## Prerequisites

1. Docker environment with swarm enabled so we can make use of Docker secrets and Docker configs. Only one node is required in the cluster.
2. A DNS record in an Amazon Route53 public hosted zone.

## IAM Authorization

1. Create a new IAM user and generate a set of access keys.
2. Use this template to assign the required IAM permissions. Fill in the `hosted-zone-id` attach the IAM policy to your IAM user:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DdnsAccess",
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "arn:aws:route53:::hostedzone/[hosted-zone-id]"
        }
    ]
}
```

## Configuration

1. Ensure you have the following configuration values on hand:
    - AWS Access Key ID
    - AWS Secret Access Key
    - Hosted Zone ID associated with your domain
    - Domain name you want to use
    - TTL in seconds for the DNS record
    - Interval in seconds to control update frequency

2. Execute `bash config-up`. The script will prompt you to enter the above items and generate docker secrets and docker configs.

## Deployment

1. Execute `docker build -t route53-ddns .` to build the docker container.
2. To start the container as a service, execute `docker stack deploy --compose-file docker-compose.yml service`.
3. Inspect the logs by running `docker service logs service_route53-ddns`.

## Teardown

1. Stop the service by running `docker service rm service_route53-ddns`
2. Optionally remove the secrets and configs by executing `bash config-down`
