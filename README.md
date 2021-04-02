# route53-ddns

Docker container that performs DDNS synchronization against a DNS record registered with Amazon Route53.

## Pre-requirements

1. Docker environment with swarm enabled so we can make use of Docker secrets and Docker configs. Only one node is required in the cluster.
2. A DNS record in Amazon Route53 already created.
3. A set of access keys that grant access to Route53 (see required IAM Permissions below).

## IAM Authorization

Use this template to assign the required IAM permissions. Fill in the `hosted-zone-id` then create the IAM policy and attach to the IAM user you'll be running the application as:

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

Generate the user's access keys and store them somewhere safe.

## Configuration

1. Ensure you have the following configuration values on hand:
- AWS Access Key ID
- AWS Secret Access Key
- Hosted Zone ID associated with your domain
- Domain name you want to use
- TTL in seconds value for the DNS record
- Interval in seconds for performing the DNS record update

2. Execute `bash config-up`. You'll be prompted to enter the above values and the script will create docker secrets and docker configs.

## Deployment

1. Clone the repository `ellis-vester/route53-ddns` the machine you'll be deploying the container.
2. Execute `docker build -t route53-ddns .` to build the docker container.
3. To start the container as a service, execute `docker stack deploy --compose-file docker-compose.yml service`
4. Inspect the logs by running `docker service logs route53-ddns_route53-ddns`

## Teardown

1. Stop the service by running `docker service rm route53-ddns_service`
2. Optionally remove the secrets and configs by executing `bash config-down`
