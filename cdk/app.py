#!/usr/bin/env python3
import aws_cdk as cdk
from stack import TraffickingAlertStack

app = cdk.App()
TraffickingAlertStack(app, "TraffickingAlertUIStack")
app.synth()
