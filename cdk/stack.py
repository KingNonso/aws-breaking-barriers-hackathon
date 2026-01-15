from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    Duration,
    RemovalPolicy
)
from constructs import Construct

class TraffickingAlertStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # DynamoDB table for incidents
        incidents_table = dynamodb.Table(
            self, "IncidentsTable",
            partition_key=dynamodb.Attribute(
                name="incident_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # GSI for querying by indicator
        incidents_table.add_global_secondary_index(
            index_name="IndicatorIndex",
            partition_key=dynamodb.Attribute(
                name="indicator_value",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        # DynamoDB table for audit logs
        audit_table = dynamodb.Table(
            self, "AuditTable",
            partition_key=dynamodb.Attribute(
                name="log_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
