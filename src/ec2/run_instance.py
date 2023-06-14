import sys
import os
import time
from typing import Literal
import boto3
import paramiko
from loguru import logger
from botocore.exceptions import ClientError

logger.add(
    "logs/ec2.log",
    rotation="10 MB",
    backtrace=True,
    diagnose=True,
    format="<green>[{time:HH:mm:ss}]</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)
INSTANCE_ID = os.environ["INSTANCE_ID"]
ec2 = boto3.client("ec2")

key = paramiko.RSAKey.from_private_key_file(f"{os.environ['RSA_KEY_PATH']}")
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def establish_ssh_connection(instance_id: str) -> None:
    instance_info = ec2.describe_instances(InstanceIds=[instance_id])
    ssh_client.connect(
        instance_info["Reservations"][0]["Instances"][0]["PublicIpAddress"],
        username="ubuntu",
        pkey=key,
    )


def wait_for_instance_running(instance_id: str) -> Literal[True]:
    while True:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instances = response["Reservations"][0]["Instances"]

        if not instances:
            raise Exception(f"Instance {instance_id} not found")

        state = instances[0]["State"]["Name"]
        if state == "running":
            break

        time.sleep(2)


def manage_instance(instance_id: str) -> None:
    if sys.argv[1] == "start":
        try:
            response = ec2.start_instances(InstanceIds=[instance_id])
            logger.info(f"Start instances response: {response}")
            wait_for_instance_running(instance_id)
            establish_ssh_connection(instance_id)
            logger.info(f"Instance {instance_id} started")
            stdin, stdout, stderr = ssh_client.exec_command(
                "sudo systemctl enable discord-bot.service && sudo systemctl start discord-bot.service"
            )
            output = stdout.read().decode("utf-8")
            logger.info(f"SSH command output: {output}")

        except ClientError as e:
            logger.error(f"Unexpected error occurred while starting the instance: {e}")

    elif sys.argv[1] == "stop":
        try:
            establish_ssh_connection(instance_id)
            stdin, stdout, stderr = ssh_client.exec_command(
                "sudo systemctl stop discord-bot.service && sudo systemctl disable discord-bot.service"
            )
            output = stdout.read().decode("utf-8")
            logger.info(f"SSH command output: {output}")
            response = ec2.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stop instances response: {response}")
            ssh_client.close()
            logger.info("SSH connection closed")

        except ClientError as e:
            logger.error(f"Unexpected error occurred while stopping the instance: {e}")


if __name__ == "__main__":
    manage_instance(INSTANCE_ID)
