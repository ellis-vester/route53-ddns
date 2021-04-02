import os
import time

from requests import get
from get_docker_secret import get_docker_secret
import boto3

# docker secrets
AwsAccessKeyId = get_docker_secret("route53_ddns_aws_access_key_id", safe=False)
AwsSecretAccessKey = get_docker_secret("route53_ddns_aws_secret_access_key", safe=False)

# docker config
HostedZoneId = get_docker_secret("route53_ddns_hosted_zone_id", safe=False, secrets_dir="/")
DomainName = get_docker_secret("route53_ddns_domain_name", safe=False, secrets_dir="/")
RecordType = get_docker_secret("route53_ddns_record_type", safe=False, secrets_dir="/")
Ttl = get_docker_secret("route53_ddns_ttl", safe=False, secrets_dir="/", cast_to=int)
Interval = get_docker_secret("route53_ddns_interval", safe=False, secrets_dir="/", cast_to=int)

def get_current_local_ip():
    return get('https://api.ipify.org').text

def get_current_route53_ip():
    client = boto3.client(
        'route53', 
        aws_access_key_id=AwsAccessKeyId,
        aws_secret_access_key=AwsSecretAccessKey)

    response = client.list_resource_record_sets(
        HostedZoneId=HostedZoneId,
        StartRecordName=DomainName,
        StartRecordType=RecordType,
        MaxItems='1'
    )

    return response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

def update_route53_ip(ipv4):
    client = boto3.client(
        'route53', 
        aws_access_key_id=AwsAccessKeyId,
        aws_secret_access_key=AwsSecretAccessKey)
    
    client.change_resource_record_sets(
        HostedZoneId=HostedZoneId,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': DomainName,
                        'Type': RecordType,
                        'TTL': Ttl,
                        'ResourceRecords': [
                            {
                                'Value': ipv4
                            }
                        ]
                    }
                }
            ]
        }
    )

if __name__ == "__main__":

    while(1):
        try:
            local_ip = get_current_local_ip()

            print("Current local IP: {}".format(local_ip))

            route53_ip = get_current_route53_ip()

            print("Current Route53 IP: {}".format(route53_ip))

            if local_ip != route53_ip:
                print("Updating Route53 record: {} => {}".format("home.body-cakes.net", local_ip))
                update_route53_ip(local_ip)
                print("Route53 record updated: {} => {}".format("home.body-cakes.net", local_ip))
            else:
                print("Local IP unchanged.")

        except Exception as e:
            print("Failed to update DNS record")
            print(str(e))

        print("Sleeping for {} seconds...".format(Interval))
        time.sleep(Interval)
