document.addEventListener("DOMContentLoaded", async () => {
    await populateDatasetList();
    initializeMap();
});

// Function to get available datasets dynamically
async function populateDatasetList() {
    await new Promise(resolve => setTimeout(resolve, 500)); // Delay in case the element loads late

    const datasetList = document.getElementById("dataset-list");
    if (!datasetList) {
        console.error("Element #dataset-list not found in DOM after waiting.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/Map_JSON/");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(await response.text(), "text/html");
        const links = [...htmlDoc.querySelectorAll("a[href$='.json']")];

        const datasetList = document.getElementById("dataset-list");
        if (!datasetList) {
            console.error("Element #dataset-list not found in DOM.");
            return;
        }
        datasetList.innerHTML = "";

        links.forEach(link => {
            const datasetName = link.textContent;
            const datasetUrl = `http://localhost:8000/Map_JSON/${datasetName}`;

            const button = document.createElement("button");
            button.textContent = datasetName;
            button.addEventListener("click", () => loadDataset(datasetUrl));
            datasetList.appendChild(button);
        });
    } catch (error) {
        console.error("Error fetching dataset list:", error);
    }
}

// Function to dynamically load datasets
async function loadDataset(jsonFile) {
    try {
        const response = await fetch(jsonFile);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();

        const controlsContainer = document.getElementById("data-controls");
        if (!controlsContainer) {
            console.error("Element #data-controls not found in DOM.");
            return;
        }

        controlsContainer.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
            console.error("Invalid dataset format: Expected an array of objects.");
            return;
        }

        const headers = Object.keys(data[0]).filter(
            key => key !== "OA_Code" && key !== "Latitude" && key !== "Longitude"
        );

        const groupedHeaders = groupHeaders(headers);

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

                const wrapper = document.createElement("div");
                wrapper.appendChild(label);
                dropdown.appendChild(wrapper);
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

        console.log(`Checking header: ${header}`);

        if (header.toLowerCase().includes("all people")) {
            category = "All People";
        } else if (header.toLowerCase().includes("male") && !header.toLowerCase().includes("female")) {
            category = "Male Only";
        } else if (header.toLowerCase().includes("female") && !header.toLowerCase().includes("male")) {
            category = "Female Only";
        }

        console.log(`Assigned category: ${category}`);

        if (category === "Other" && header.toLowerCase().includes("female")) {
            category = "Female Only";
        }

        if (!groups[category]) groups[category] = [];
        groups[category].push(header);
    });

    console.log('Grouped headers:', groups);

    return groups;
}

// Initialize Leaflet Map
function initializeMap() {
    const map = L.map('map').setView([55.3781, -3.4360], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetch("http://localhost:8000/Map_JSON/output.UV103_Age_by_Single_Year.json")
        .then(response => response.json())
        .then(data => {
            const layerGroups = {};

            data.forEach(entry => {
                const lat = parseFloat(entry.Latitude);
                const lon = parseFloat(entry.Longitude);

                if (isNaN(lat) || isNaN(lon)) return;

                const marker = L.circleMarker([lat, lon], { radius: 5, color: 'blue' });
                marker.entry = entry;
                marker.bindPopup(`OA Code: ${entry.OA_Code}`);

                Object.keys(entry).forEach(key => {
                    if (!["OA_Code", "Latitude", "Longitude"].includes(key)) {
                        if (!layerGroups[key]) layerGroups[key] = L.layerGroup();
                        layerGroups[key].addLayer(marker);
                    }
                });
            });

            document.querySelectorAll("input[type='checkbox']").forEach(checkbox => {
                let key = checkbox.dataset.dataset;
                checkbox.addEventListener('change', () => {
                    checkbox.checked ? map.addLayer(layerGroups[key]) : map.removeLayer(layerGroups[key]);
                });
            });
        })
        .catch(error => console.error("Error fetching dataset:", error));
}

// Functions to handle dataset toggling
function fetchDataset(dataset) {
    console.log(`Fetching dataset: ${dataset}`);
}

function removeDataset(dataset) {
    console.log(`Removing dataset: ${dataset}`);
}