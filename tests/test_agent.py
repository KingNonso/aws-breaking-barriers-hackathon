"""
Unit tests for agent functionality
Tests will be implemented in tasks 11-12
"""

import pytest
import sys
import os

# Add lambda directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from agent import extract_networks, check_multi_source, get_recommendations


class TestHelperFunctions:
    """Test helper functions for data operations"""
    
    def test_extract_networks_with_network_ids(self):
        """Test extracting network IDs from incidents"""
        incidents = [
            {'incident_id': '1', 'network_id': 'NET-001'},
            {'incident_id': '2', 'network_id': 'NET-002'},
            {'incident_id': '3', 'network_id': 'NET-001'},  # Duplicate
            {'incident_id': '4'}  # No network_id
        ]
        
        result = extract_networks(incidents)
        
        # Should return unique network IDs
        assert len(result) == 2
        network_ids = {n['id'] for n in result}
        assert 'NET-001' in network_ids
        assert 'NET-002' in network_ids
    
    def test_extract_networks_empty(self):
        """Test extracting networks from empty list"""
        result = extract_networks([])
        assert result == []
    
    def test_extract_networks_no_network_ids(self):
        """Test extracting networks when no network_ids present"""
        incidents = [
            {'incident_id': '1'},
            {'incident_id': '2'}
        ]
        result = extract_networks(incidents)
        assert result == []
    
    def test_check_multi_source_true(self):
        """Test detecting multi-source indicators"""
        incident = {'source': 'tip_line'}
        context = {
            'matching_incidents': [
                {'source': 'financial_monitoring'},
                {'source': 'social_media'}
            ]
        }
        
        result = check_multi_source(incident, context)
        assert result is True
    
    def test_check_multi_source_false(self):
        """Test single source indicator"""
        incident = {'source': 'tip_line'}
        context = {
            'matching_incidents': [
                {'source': 'tip_line'},
                {'source': 'tip_line'}
            ]
        }
        
        result = check_multi_source(incident, context)
        assert result is False
    
    def test_check_multi_source_empty_context(self):
        """Test multi-source check with empty context"""
        incident = {'source': 'tip_line'}
        context = {}
        
        result = check_multi_source(incident, context)
        assert result is False
    
    def test_get_recommendations_urgent(self):
        """Test recommendations for URGENT classification"""
        result = get_recommendations("URGENT - Victim at Risk")
        
        assert "Immediate victim rescue" in result
        assert "Suspect apprehension" in result
        assert "Coordinate with FBI" in result
    
    def test_get_recommendations_priority(self):
        """Test recommendations for PRIORITY classification"""
        result = get_recommendations("PRIORITY - Investigation Needed")
        
        assert "Begin investigation" in result
        assert "Surveillance of suspect" in result
        assert "Monitor for escalation" in result
    
    def test_get_recommendations_monitor(self):
        """Test recommendations for MONITOR classification"""
        result = get_recommendations("MONITOR - Log for Pattern Analysis")
        
        assert "Log for pattern analysis" in result
        assert "Monitor for repeat indicators" in result


# Placeholder for additional tests
# More tests will be added in subsequent tasks
