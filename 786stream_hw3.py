import streamlit as st

st.title("Real-Time Speedometer and Distance Tracker")
st.markdown("""
This app tracks your real-time speed and total distance traveled.  
Ensure you allow GPS access and keep the app open during your journey.
""")

gps_speedometer_script = """
<script>
let prevLat = null;
let prevLng = null;
let prevTime = null;
let totalDistance = 0;

function toRadians(degrees) {
    return degrees * Math.PI / 180;
}

function haversine(lat1, lng1, lat2, lng2) {
    const R = 6371e3; // Radius of the Earth in meters
    const phi1 = toRadians(lat1);
    const phi2 = toRadians(lat2);
    const deltaPhi = toRadians(lat2 - lat1);
    const deltaLambda = toRadians(lng2 - lng1);

    const a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
              Math.cos(phi1) * Math.cos(phi2) *
              Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // Distance in meters
}

function updateLocation(position) {
    const currentLat = position.coords.latitude;
    const currentLng = position.coords.longitude;
    const currentTime = position.timestamp;

    if (prevLat !== null && prevLng !== null && prevTime !== null) {
        const distance = haversine(prevLat, prevLng, currentLat, currentLng);
        const timeElapsed = (currentTime - prevTime) / 1000; // Time in seconds

        if (timeElapsed > 0) {
            const speed = (distance / timeElapsed) * 3.6; // Speed in km/h
            totalDistance += distance;

            document.getElementById("speed").innerHTML = `Speed: ${speed.toFixed(2)} km/h`;
            document.getElementById("distance").innerHTML = `Total Distance: ${(totalDistance / 1000).toFixed(2)} km`;
        }
    }

    prevLat = currentLat;
    prevLng = currentLng;
    prevTime = currentTime;
}

function handleError(error) {
    document.getElementById("speed").innerHTML = "Unable to access GPS.";
    document.getElementById("distance").innerHTML = "Please enable GPS.";
}

if (navigator.geolocation) {
    navigator.geolocation.watchPosition(updateLocation, handleError, { enableHighAccuracy: true });
} else {
    document.getElementById("speed").innerHTML = "Geolocation is not supported by this browser.";
    document.getElementById("distance").innerHTML = "";
}
</script>
<div>
    <p id="speed">Speed: Waiting for GPS...</p>
    <p id="distance">Total Distance: Waiting for GPS...</p>
</div>
"""

st.components.v1.html(gps_speedometer_script, height=200)
