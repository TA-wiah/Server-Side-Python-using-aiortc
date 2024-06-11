# WebRTC Python Project

# Overview
This project demonstrates a simple WebRTC application where a client PC connects to a server PC to view its camera feed. The communication between the client and server is facilitated using WebRTC's RTCPeerConnection. The project includes both server-side and client-side components.

## Client-Side Explanation

# RTCPeerConnection
RTCPeerConnection: Represents a WebRTC connection to another PC. It handles the connection establishment, media exchange, and data communication.
ontrack
ontrack: Event handler for incoming media streams. When the remote stream is received, it is added to the HTML video element to display the media.
connect
connect: Fetches the offer from the server, sets the remote description, creates an answer, and sets the local description. This sequence establishes the WebRTC connection between the client and server.
Running the Example
Prerequisites
A server PC with a camera.
A client PC to access the camera feed.
A web server (e.g., Apache, Nginx) to serve the HTML/JavaScript file.
Steps
Server-Side Setup:

    Replace your_server_ip with the IP address of the server PC in the client-side script.
Run the server-side Python script on the server PC with the camera.
Client-Side Setup:

S# erve the HTML/JavaScript file from any web server accessible to the client PC.
Access the HTML file from a web browser on the client PC. You should see the camera feed from the server PC.

# Credits
Created by cyberhatcher (Jeffrey).
