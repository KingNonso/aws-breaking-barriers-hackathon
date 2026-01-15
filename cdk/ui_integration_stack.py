from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigwv2,
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import os

class UIIntegrationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # S3 bucket for static website
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            website_index_document="screen1.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        
        # CloudFront distribution
        distribution = cloudfront.Distribution(
            self, "WebsiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="screen1.html",
        )
        
        # DynamoDB tables
        incidents_table = dynamodb.Table(
            self, "IncidentsTable",
            partition_key=dynamodb.Attribute(
                name="incident_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        
        connections_table = dynamodb.Table(
            self, "ConnectionsTable",
            partition_key=dynamodb.Attribute(
                name="connection_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        
        connections_table.add_global_secondary_index(
            index_name="incident_id-index",
            partition_key=dynamodb.Attribute(
                name="incident_id",
                type=dynamodb.AttributeType.STRING
            ),
        )
        
        # Lambda functions
        submit_lambda = lambda_.Function(
            self, "SubmitIncidentLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="submit_incident.lambda_handler",
            code=lambda_.Code.from_asset("lambda/ui_integration"),
            environment={
                "INCIDENTS_TABLE": incidents_table.table_name,
            },
            timeout=Duration.seconds(30),
        )
        
        status_lambda = lambda_.Function(
            self, "StatusQueryLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="status_query.lambda_handler",
            code=lambda_.Code.from_asset("lambda/ui_integration"),
            environment={
                "INCIDENTS_TABLE": incidents_table.table_name,
            },
            timeout=Duration.seconds(30),
        )
        
        pdf_lambda = lambda_.Function(
            self, "PDFGenerationLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="pdf_generation.lambda_handler",
            code=lambda_.Code.from_asset("lambda/ui_integration"),
            environment={
                "INCIDENTS_TABLE": incidents_table.table_name,
            },
            timeout=Duration.seconds(30),
        )
        
        # Grant permissions
        incidents_table.grant_read_write_data(submit_lambda)
        incidents_table.grant_read_data(status_lambda)
        incidents_table.grant_read_data(pdf_lambda)
        
        submit_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=["*"],
            )
        )
        
        # REST API Gateway
        api = apigw.RestApi(
            self, "UIIntegrationAPI",
            rest_api_name="Trafficking Alert UI API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )
        
        incidents = api.root.add_resource("incidents")
        incidents.add_method("POST", apigw.LambdaIntegration(submit_lambda))
        
        incident = incidents.add_resource("{incident_id}")
        incident.add_method("GET", apigw.LambdaIntegration(status_lambda))
        
        brief = incident.add_resource("brief")
        brief.add_method("GET", apigw.LambdaIntegration(pdf_lambda))
        
        # WebSocket API
        ws_connect_lambda = lambda_.Function(
            self, "WSConnectLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="connection_handler.connect_handler",
            code=lambda_.Code.from_asset("lambda/websocket"),
            environment={
                "CONNECTIONS_TABLE": connections_table.table_name,
            },
        )
        
        ws_disconnect_lambda = lambda_.Function(
            self, "WSDisconnectLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="connection_handler.disconnect_handler",
            code=lambda_.Code.from_asset("lambda/websocket"),
            environment={
                "CONNECTIONS_TABLE": connections_table.table_name,
            },
        )
        
        connections_table.grant_read_write_data(ws_connect_lambda)
        connections_table.grant_read_write_data(ws_disconnect_lambda)
        
        ws_api = apigwv2.CfnApi(
            self, "WebSocketAPI",
            name="Trafficking Alert WebSocket",
            protocol_type="WEBSOCKET",
            route_selection_expression="$request.body.action",
        )
        
        # Outputs
        CfnOutput(self, "WebsiteURL", value=f"https://{distribution.distribution_domain_name}")
        CfnOutput(self, "APIURL", value=api.url)
        CfnOutput(self, "WebSocketURL", value=f"wss://{ws_api.ref}.execute-api.{self.region}.amazonaws.com/prod")
        CfnOutput(self, "BucketName", value=website_bucket.bucket_name)
