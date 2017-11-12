import boto3
from botocore.exceptions import ClientError
from const.const import Constants
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.instance import EC2InstanceModel


class ManagerManual(Resource):
    """ManagerManual provides API for manager to manually control userUI worker pool.

        Attributes:
            parser (RequestParser): The Flask-RESTful request parser.
            It parses action (grow/shrink) from the JSON payload for worker pool control.
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'action',
        type=str,
        required=True
    )

    parser.add_argument(
        'instance',
        type=str
    )

    @jwt_required()
    def post(self):
        """Grow or shrink a worker. (POST)

        This method grows or shrinks the worker pool by 1, according to
        'action' and 'instance' parameter in the request JSON body.

        Returns:
            (JSON): Worker pool grow/shrink success or fail message.
            (int): HTTP status code.
        """
        # special treat for manager
        if current_identity.id != Constants.MANAGER_DATABASE_ID:
            return {'message': 'you are not manager'}, 403

        # parse request JSON 'action'
        data = ManagerManual.parser.parse_args()
        action = data.get('action', '').lower()
        if action == '' or (action != 'grow' and action != 'shrink'):
            return {'message': 'invalid action (grow/shrink)'}, 400

        # create or delete instance
        elb = boto3.client('elb')

        # create and start an EC2 instance from AMI
        if action == 'grow':
            # resource
            ec2_resource = boto3.resource('ec2')

            # database existing
            existing = EC2InstanceModel.get_all()
            count = len(existing)+1

            try:
                created = ec2_resource.create_instances(
                    ImageId=Constants.USER_WORKER_IMAGE_ID,
                    InstanceType='t2.small',
                    KeyName=Constants.KEY_NAME,
                    MaxCount=1,
                    MinCount=1,
                    Monitoring={
                        'Enabled': True
                    },
                    SecurityGroups=[
                        Constants.SECURITY_GROUP,
                    ],
                    DryRun=False,
                    InstanceInitiatedShutdownBehavior='terminate',
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'A2-UserWorker-%03d' % count
                                },
                            ]
                        },
                    ]
                )
            except IOError:
                return {'message': 'internal server error'}, 500

            instance = created[0].id

            # add to ELB
            try:
                elb.register_instances_with_load_balancer(
                    LoadBalancerName=Constants.ELB_NAME,
                    Instances=[
                        {
                            'InstanceId': instance
                        },
                    ]
                )
            except IOError:
                return {'message': 'internal server error'}, 500

            # add to database
            try:
                item = EC2InstanceModel(instance)
                item.save_to_db()
            except IOError:
                return {'message': 'internal server error'}, 500

        # stop and terminate an instance
        else:
            # client
            ec2_client = boto3.client('ec2')

            # parse request JSON 'instance'
            instance = data.get('instance', '').lower()
            instances = []
            for item in EC2InstanceModel.get_all():
                instances.append(item.instance)
            if instance == '' or instance not in instances:
                return {'message': 'invalid instance id'}, 400

            # try a dry run first to verify permissions
            try:
                ec2_client.terminate_instances(InstanceIds=[instance], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

            # dry run succeeded, run terminate_instances for real
            try:
                response = ec2_client.terminate_instances(InstanceIds=[instance], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)

            # remove from ELB
            try:
                elb.deregister_instances_from_load_balancer(
                    LoadBalancerName=Constants.ELB_NAME,
                    Instances=[
                        {
                            'InstanceId': instance
                        },
                    ]
                )
            except IOError:
                return {'message': 'internal server error'}, 500

            # remove from database
            try:
                item = EC2InstanceModel.find_by_instance_id(instance)
                item.delete_from_db()
            except IOError:
                return {'message': 'internal server error'}, 500

        return {'message': 'action %s performed successfully' % action}, 200
