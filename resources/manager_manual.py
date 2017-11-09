import boto3
from botocore.exceptions import ClientError
from const.const import Constants
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity


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
        type=str,
        required=True
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
        if current_identity.id != Constants.MANAGER_ID:
            return {'message': 'you are not manager'}, 403

        # parse request JSON
        data = ManagerManual.parser.parse_args()
        action = data.get('action', '').lower()
        if action == '' or (action != 'grow' and action != 'shrink'):
            return {'message': 'invalid action (grow/shrink)'}, 400
        instance = data.get('instance', '').lower()
        if instance == '' or instance not in Constants.INSTANCES.values():
            return {'message': 'invalid instance id'}, 400

        # change instance state
        ec2 = boto3.client('ec2')
        if action == 'grow':
            # try a dry run first to verify permissions
            try:
                ec2.start_instances(InstanceIds=[instance], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise
            # dry run succeeded, run start_instances without dry run
            try:
                response = ec2.start_instances(InstanceIds=[instance], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)
        else:
            # try a dry run first to verify permissions
            try:
                ec2.stop_instances(InstanceIds=[instance], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise
            # dry run succeeded, run start_instances without dry run
            try:
                response = ec2.stop_instances(InstanceIds=[instance], DryRun=False)
                print(response)
            except ClientError as e:
                print(e)

        return {'message': 'action %s performed successfully' % action}, 200
