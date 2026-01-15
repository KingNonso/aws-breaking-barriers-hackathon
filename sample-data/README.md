# Sample Incident Data

This directory contains sample EventBridge events for testing the Trafficking Alert Agent.

## Files

- `sample-incident.json` - Medium priority phone number indicator from tip line
- `sample-incident-urgent.json` - High priority phone number with known network link
- `sample-incident-monitor.json` - Low priority suspect name from social media

## Usage

To test the agent with sample incidents, use the AWS CLI:

```bash
# Test with standard incident
aws events put-events --entries file://sample-data/sample-incident.json

# Test with urgent incident
aws events put-events --entries file://sample-data/sample-incident-urgent.json

# Test with monitor-only incident
aws events put-events --entries file://sample-data/sample-incident-monitor.json
```

## Event Structure

Each event follows this structure:

```json
{
  "Source": "trafficking.indicators",
  "DetailType": "Phone Number | Suspect Name | Transaction Pattern",
  "Detail": {
    "indicator_type": "phone | name | transaction",
    "value": "string",
    "source": "tip_line | financial_monitoring | social_media",
    "metadata": {}
  }
}
```

## Testing Scenarios

1. **Standard Flow**: Use `sample-incident.json` to test normal processing
2. **Urgent Alert**: Use `sample-incident-urgent.json` to trigger high-priority routing
3. **Monitor Only**: Use `sample-incident-monitor.json` to test logging without alerts
