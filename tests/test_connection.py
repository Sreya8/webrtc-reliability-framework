from playwright.sync_api import Page
import time

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


def test_create_sdp_offer(page: Page):
    """
    Generate an SDP offer — the first real step of a WebRTC call.
    
    When FaceTime calls someone, the caller's device creates an SDP offer
    describing what it can do. This is the document that gets sent through
    the signaling server to the other device.
    
    We measure how long this takes — slow SDP generation = slow call setup.
    """
    page.goto("about:blank")

    start = time.time()

    result = page.evaluate("""
        async () => {
            const config = {iceServers: [{ urls: 'stun:stun.l.google.com:19302'}]};
            
            const pc = new RTCPeerConnection(config);
            
            // createOffer() generates the SDP document
            // It's async — takes a moment to generate
            const offer = await pc.createOffer();
            
            // setLocalDescription() tells the peer connection
            // "this is MY side of the negotiation"
            await pc.setLocalDescription(offer);
            
            return {
                    sdpType: offer.type,
                    sdpLength: offer.sdp.length,
                    signalingState: pc.signalingState,
                    sdpPreview: offer.sdp.substring(0, 150)
            };
        }
    """)

    elapsed = round(time.time() - start, 3)

    print(f"\nSDP offer created in {elapsed}s")
    print(f"  SDP type:         {result['sdpType']}")
    print(f"  SDP length:       {result['sdpLength']} characters")
    print(f"  Signaling state:  {result['signalingState']}")
    print(f"\nSDP document preview:")
    print(f"{result['sdpPreview']}")

    assert result['sdpType'] == 'offer'
    assert result['sdpLength'] > 0
    assert result['signalingState'] == 'have-local-offer'
    assert elapsed < 5.0, f"SDP generation too slow: {elapsed}s"
