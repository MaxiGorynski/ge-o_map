// Start a local server first if needed (e.g., python3 -m http.server 8000)

// Ensure this script runs AFTER the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    loadDataset("http://localhost:8000/Map_JSON/output.UV101b_Usual_Resident_Population_By_Age_and_Sex.json");
    initializeMap();
});

// Function to dynamically load datasets
async function loadDataset(jsonFile) {
    try {
        const response = await fetch(jsonFile);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();

        // Ensure the dataset control container exists
        const controlsContainer = document.getElementById("data-controls");
        if (!controlsContainer) {
            console.error("Element #dataset-controls not found in DOM.");
            return;
        }

        controlsContainer.innerHTML = ""; // Reset UI

        if (!Array.isArray(data) || data.length === 0) {
            console.error("Invalid dataset format: Expected an array of objects.");
            return;
        }

        // Extract dataset keys dynamically
        const headers = Object.keys(data[0]).filter(
            key => key !== "OA_Code" && key !== "Latitude" && key !== "Longitude"
        );

        const groupedHeaders = groupHeaders(headers);

        // Populate UI dynamically
        Object.keys(groupedHeaders).forEach(category => {
            const details = document.createElement("details");
            const summary = document.createElement("summary");
            summary.textContent = category;
            details.appendChild(summary);

            const dropdown = document.createElement("div");
            dropdown.classList.add("dropdown-content");

            groupedHeaders[category].forEach(dataset => {
                const label = document.createElement("label");
                const checkbox = document.createElement("input");

                checkbox.type = "checkbox";
                checkbox.id = `toggle-${dataset.replace(/\s+/g, "-").toLowerCase()}`;
                checkbox.setAttribute("data-dataset", dataset);
                checkbox.checked = false;

                checkbox.addEventListener("change", () => {
                    if (checkbox.checked) {
                        fetchDataset(dataset);
                    } else {
                        removeDataset(dataset);
                    }
                });

                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(dataset));

                // Wrap each label and checkbox in a div to ensure a line break
                const wrapper = document.createElement("div");
                wrapper.appendChild(label);
                dropdown.appendChild(wrapper); // Add wrapper to dropdown content
            });

            details.appendChild(dropdown);
            controlsContainer.appendChild(details);
        });

    } catch (error) {
        console.error("Error loading dataset:", error);
    }
}

// Function to group dataset headers
function groupHeaders(headers) {
    const groups = {};

    headers.forEach(header => {
        let category = "Other";

        // Categorize "All People", "Male Only", "Female Only"
        if (header.toLowerCase().includes("all people")) category = "All People";
        else if (header.toLowerCase().includes("male")) category = "Male Only";
        else if (header.toLowerCase().includes("female")) category = "Female Only";

        if (!groups[category]) groups[category] = [];
        groups[category].push(header);
    });

    return groups;
}


// Initialize Leaflet Map
function initializeMap() {
    const map = L.map('map').setView([55.3781, -3.4360], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetch("http://localhost:8000/Map_JSON/output.UV101b_Usual_Resident_Population_By_Age_and_Sex.json")
        .then(response => response.json())
        .then(data => {
            const layerGroups = {};

            data.forEach(entry => {
                const lat = parseFloat(entry.Latitude);
                const lon = parseFloat(entry.Longitude);

                if (isNaN(lat) || isNaN(lon)) {
                    console.warn("Skipping entry with invalid coordinates:", entry);
                    return;
                }

                const marker = L.circleMarker([lat, lon], {
                    radius: 5,
                    color: 'blue'
                });

                marker.entry = entry; // Store the dataset entry on the marker
                marker.bindPopup(`OA Code: ${entry.OA_Code}`);

                // Add marker to all relevant layer groups
                Object.keys(entry).forEach(key => {
                    if (key !== "OA_Code" && key !== "Latitude" && key !== "Longitude") {
                        if (!layerGroups[key]) {
                            layerGroups[key] = L.layerGroup();
                        }
                        layerGroups[key].addLayer(marker);
                    }
                });
            });

            // Add layer control to map
            //L.control.layers(null, layerGroups, { collapsed: false }).addTo(map);

            // Handle checkbox toggles for layers
            document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {
                let key = checkbox.dataset.dataset;

                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        map.addLayer(layerGroups[key]);
                    } else {
                        map.removeLayer(layerGroups[key]);
                    }
                });
            });

            // Dynamically update popups based on active toggles
            map.on('popupopen', function (e) {
                const marker = e.popup._source;
                const entry = marker.entry;

                let popupContent = `OA Code: ${entry.OA_Code}<br>`;

                document.querySelectorAll("input[type='checkbox']:checked").forEach(checkbox => {
                    let datasetKey = checkbox.dataset.dataset;
                    if (entry.hasOwnProperty(datasetKey)) {
                        popupContent += `${datasetKey}: ${entry[datasetKey]}<br>`;
                    }
                });

                marker.setPopupContent(popupContent);
            });

           // Dynamically update popups based on active toggles
            map.on('popupopen', function (e) {
                const marker = e.popup._source;
                const entry = marker.entry;

                let popupContent = `OA Code: ${entry.OA_Code}<br>`;

                // Loop through all checked checkboxes and display their corresponding data values
                document.querySelectorAll("input[type='checkbox']:checked").forEach(checkbox => {
                    let datasetKey = checkbox.dataset.dataset;
                    if (entry.hasOwnProperty(datasetKey)) {
                        popupContent += `${datasetKey}: ${entry[datasetKey]}<br>`;
                    }
                });

                marker.setPopupContent(popupContent);
            });
        })
        .catch(error => console.error("Error loading map data:", error));
}

// Functions to handle dataset toggling
function fetchDataset(dataset) {
    console.log(`Fetching dataset: ${dataset}`);
}

function removeDataset(dataset) {
    console.log(`Removing dataset: ${dataset}`);
}