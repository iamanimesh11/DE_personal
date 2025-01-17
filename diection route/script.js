    let map, marker, routeControl;
    let trackingActive = false;
    let destinationLat, destinationLon;
    let gpsEnabled = false;

    // Initialize the map
    function initializeMap() {
      map = L.map('map').setView([20.5937, 78.9629], 5); // Default location: India
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
      }).addTo(map);
    }

    // Start real-time tracking and calculate the route
    function startTracking() {
      if (trackingActive) {
        alert("Location tracking is already active.");
        return;
      }
      trackingActive = true;  // Mark tracking as active

      // Get the coordinates from the user input
      const coordinates = document.getElementById('coordinates').value;
      const coordsArray = coordinates.split(',').map(coord => parseFloat(coord.trim()));

      if (coordsArray.length === 2 && !isNaN(coordsArray[0]) && !isNaN(coordsArray[1])) {
        destinationLat = coordsArray[0];
        destinationLon = coordsArray[1];

        // Set up route from current location to the entered destination
        if (routeControl) {
          map.removeControl(routeControl); // Remove previous route
        }

        routeControl = L.Routing.control({
          waypoints: [
            L.latLng(20.5937, 78.9629),  // Default start location
            L.latLng(destinationLat, destinationLon)  // Destination coordinates
          ],
          routeWhileDragging: true
        }).addTo(map);
      } else {
        alert("Please enter valid coordinates in the format: Latitude, Longitude");
        return;
      }

      // Handle location tracking
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
          (position) => {
            gpsEnabled = true;
            const { latitude, longitude } = position.coords;

            // Update marker position
            if (!marker) {
              marker = L.marker([latitude, longitude]).addTo(map);
            } else {
              marker.setLatLng([latitude, longitude]);
            }

            // Update the map view
            map.setView([latitude, longitude], 15);

            // Update route to destination
            routeControl.setWaypoints([
              L.latLng(latitude, longitude), // Update start location
              L.latLng(destinationLat, destinationLon)  // Destination
            ]);
          },
          (err) => {
            console.error("Error getting location:", err);
            alert("Unable to get location. Please check GPS.");
          },
          { enableHighAccuracy: true }
        );
      } else {
        alert("Geolocation not supported by your browser.");
      }
    }

    // Initialize the map when the page loads
    initializeMap();
