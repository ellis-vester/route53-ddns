import boto3
from requests import get
import os
import time

# Required
HostedZoneId = os.environ['HOSTED_ZONE_ID']
DnsRecordName = os.environ['DNS_RECORD_NAME']

# Optional
RecordType = os.environ['RECORD_TYPE'] or 'A'
Ttl = int(os.environ['TTL']) or 600
Interval = int(os.environ['INTERVAL']) or 300

def get_docker_secret(file):
    if not os.path.isfile("/run/secrets/{}".format(file)):
        raise Exception("Could not read {} secret".format(file))
    return open("/run/secrets/{}".format(file), "r").read()

AwsAccessKeyId = get_docker_secret("aws_access_key_id")
AwsSecretAccessKey = get_docker_secret("aws_secret_access_key")

def get_current_local_ip():
    return get('https://api.ipify.org').text

def get_current_route53_ip():
    client = boto3.client(
        'route53', 
        aws_access_key_id=AwsAccessKeyId,
        aws_secret_access_key=AwsSecretAccessKey)

    response = client.list_resource_record_sets(
        HostedZoneId=HostedZoneId,
        StartRecordName=DnsRecordName,
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
                        'Name': DnsRecordName,
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

        time.sleep(Interval)
