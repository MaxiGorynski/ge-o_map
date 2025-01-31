// Start a local server first if needed (e.g., python3 -m http.server 8000)

// Ensure this script runs AFTER the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    loadDataset("http://localhost:8000/Map_JSON/output.UV102b_Age_by_Sex.json");
    initializeMap();
});

// Function to dynamically load datasets
async function loadDataset(jsonFile) {
    try {
        const response = await fetch(jsonFile);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();

        // Ensure the dataset control container exists
        const controlsContainer = document.getElementById("dataset-controls");
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

                dropdown.appendChild(label);
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

    fetch("http://localhost:8000/Map_JSON/output.UV101b_Usual_Resident_Population_by_Sex_and_Age.json")
        .then(response => response.json())
        .then(data => {
            const layerGroups = {};
            const datasetMapping = {};

            // Add each data entry to a map layer dynamically
            data.forEach(entry => {
                const lat = parseFloat(entry.Latitude);
                const lon = parseFloat(entry.Longitude);

                if (isNaN(lat) || isNaN(lon)) {
                    console.warn("Skipping entry with invalid coordinates:", entry);
                    return;
                }

                // Create a marker for each location
                const marker = L.circleMarker([lat, lon], {
                    radius: 5,
                    color: 'blue'
                });

                marker.bindPopup(`OA Code: ${entry.OA_Code}`);

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
            let layerControl = L.control.layers(null, layerGroups, { collapsed: false }).addTo(map);

            // Add event listeners to checkboxes
            document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {
                let key = checkbox.dataset.dataset;
                datasetMapping[key] = checkbox;

                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        map.addLayer(layerGroups[key]);
                    } else {
                        map.removeLayer(layerGroups[key]);
                    }
                });
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