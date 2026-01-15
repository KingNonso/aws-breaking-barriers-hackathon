// Unit tests for Session Manager
const SessionManager = require('../js/session-manager');

describe('SessionManager', () => {
  let sessionManager;
  
  beforeEach(() => {
    sessionManager = new SessionManager();
    localStorage.clear();
  });

  test('saveSession stores data', () => {
    sessionManager.saveSession('incident-123', 'screen2');
    
    const stored = localStorage.getItem('trafficking_alert_session');
    expect(stored).toBeTruthy();
    
    const data = JSON.parse(stored);
    expect(data.incident_id).toBe('incident-123');
    expect(data.current_screen).toBe('screen2');
  });

  test('getSession retrieves valid session', () => {
    sessionManager.saveSession('incident-123', 'screen2');
    
    const session = sessionManager.getSession();
    expect(session.incident_id).toBe('incident-123');
    expect(session.current_screen).toBe('screen2');
  });

  test('getSession returns null for expired session', () => {
    const oldSession = {
      incident_id: 'incident-123',
      current_screen: 'screen2',
      timestamp: Date.now() - (2 * 60 * 60 * 1000) // 2 hours ago
    };
    localStorage.setItem('trafficking_alert_session', JSON.stringify(oldSession));
    
    const session = sessionManager.getSession();
    expect(session).toBeNull();
  });

  test('clearSession removes data', () => {
    sessionManager.saveSession('incident-123', 'screen2');
    sessionManager.clearSession();
    
    const stored = localStorage.getItem('trafficking_alert_session');
    expect(stored).toBeNull();
  });

  test('isSessionActive checks validity', () => {
    expect(sessionManager.isSessionActive()).toBe(false);
    
    sessionManager.saveSession('incident-123', 'screen2');
    expect(sessionManager.isSessionActive()).toBe(true);
  });
});
