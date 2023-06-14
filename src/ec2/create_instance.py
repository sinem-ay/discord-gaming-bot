import boto3


ec2 = boto3.resource("ec2")

instances = ec2.create_instances(
    ImageId="ami-0dafa01c8100180f8",  # Amazon Machine Image ID - ubuntu 22.04
    MinCount=1,  # Min number of instances you want to create
    MaxCount=1,  # Max number of instances you want to create
    InstanceType="t2.micro",  # Free-tier eligable instance type
    KeyName="python-discord-bot-key",  # Name of the key pair, to access instance. You can either create in AWS Management Console EC2 > Network & Security - Key Pairs or in AWS CLI with aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem
)
