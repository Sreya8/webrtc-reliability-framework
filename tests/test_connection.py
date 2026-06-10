from playwright.sync_api import Page

def test_webrtc_is_supported(page: Page):
    """
    Verify WebKit supports the RTCPeerConnection API.
    This is the foundation of FaceTime — if this doesn't exist,
    nothing else works.
    """
    # Navigate to a blank page — we don't need a website
    # We just need a browser context to run JavaScript in
    page.goto("about:blank")

    # page.evaluate() runs JavaScript inside the browser
    # and returns the result to Python
    # We're asking: does RTCPeerConnection exist in this browser?
    is_supported = page.evaluate("""
        () => {
            return typeof RTCPeerConnection !== 'undefined';
        }
    """)
    print(f"\nWebRTC supported in WebKit: {is_supported}")
    assert is_supported, "RTCPeerConnection not found - WebKit does not support WebRTC"


def test_create_peer_connection(page: Page):
    """
    Create a real RTCPeerConnection object in WebKit.
    This is the first thing FaceTime does when you tap the call button.
    
    RTCPeerConnection is the core WebRTC object that:
    - holds the connection state
    - manages ICE candidates
    - handles media tracks
    - controls encryption
    """
    page.goto("about:blank")

    # Create a peer connection and check its initial state
    # ICE servers are STUN servers — we'll use Google's public one for now

    result = page.evaluate("""
        () => {
                 const config = {
                    iceServers: [{ urls: 'stun:stun.l.google.com:19302'}]      
                };        
            
            const pc = new RTCPeerConnection(config);
            
            return {
                    connectionState: pc.connectionState,
                    iceConnectionState: pc.iceConnectionState,
                    signalingState: pc.signalingState,
                    created: true
                };
            }
    """)

    print(f"\nPeer connection created:")
    print(f"    Connection State:       {result['connectionState']}")
    print(f"    Ice Connection State:   {result['iceConnectionState']}")
    print(f"    Signaling State:        {result['signalingState']}")

    assert result['created'] == True
    assert result['connectionState'] == 'new'
    assert result['signalingState'] == 'stable'