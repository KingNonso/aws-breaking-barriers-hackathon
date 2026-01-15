// Unit tests for API Client
const APIClient = require('../js/api-client');

describe('APIClient', () => {
  let apiClient;
  
  beforeEach(() => {
    apiClient = new APIClient('https://api.test.com');
    global.fetch = jest.fn();
  });

  test('submitIncident sends correct request', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ incident_id: '123', status: 'processing' })
    });

    const result = await apiClient.submitIncident('phone', '+1234567890', 'web_ui');
    
    expect(global.fetch).toHaveBeenCalledWith(
      'https://api.test.com/incidents',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
    );
    expect(result.incident_id).toBe('123');
  });

  test('getIncidentStatus fetches status', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'complete' })
    });

    const result = await apiClient.getIncidentStatus('123');
    
    expect(global.fetch).toHaveBeenCalledWith('https://api.test.com/incidents/123');
    expect(result.status).toBe('complete');
  });

  test('handles API errors', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    });

    await expect(apiClient.submitIncident('phone', '123', 'web_ui'))
      .rejects.toThrow('API Error: 500');
  });
});
