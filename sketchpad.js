document.addEventListener("DOMContentLoaded", async () => {
    console.log("📌 DOM fully loaded. Initializing...");
    try {
        await populateDatasetList();
        console.log("✅ Dataset list populated.");
    } catch (err) {
        console.error("❌ Error populating dataset list:", err);
    }

    initializeMap();
    console.log("✅ Map initialized.");
});

// Check for dataset-list before proceeding
async function waitForElement(selector, timeout = 3000) {
    console.log(`⏳ Waiting for element: ${selector}`);
    return new Promise((resolve, reject) => {
        const start = Date.now();
        const check = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(check);
                console.log(`✅ Element found: ${selector}`);
                resolve(element);
            }
            if (Date.now() - start >= timeout) {
                clearInterval(check);
                console.error(`❌ Timeout: Element ${selector} not found in DOM.`);
                reject(new Error(`Timeout: Element ${selector} not found in DOM.`));
            }
        }, 100); // Check every 100ms
    });
}

// Function to get available datasets dynamically
async function populateDatasetList() {
    console.log("✅ populateDatasetList called");
    console.log("📥 Fetching dataset list from server...");

    try {
        const response = await fetch("http://localhost:8000/Map_JSON/");
        console.log("📥 Response received for dataset list:", response);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const parser = new DOMParser();
        const htmlText = await response.text();
        console.log("📄 Raw HTML fetched:", htmlText.substring(0, 500)); // Show first 500 chars to debug

        const htmlDoc = parser.parseFromString(htmlText, "text/html");
        const links = [...htmlDoc.querySelectorAll("a[href$='.json']")];
        console.log(`🔗 Found ${links.length} dataset links.`);

        const datasetList = document.getElementById("dataset-list");
        if (!datasetList) {
            console.error("❌ Element #dataset-list not found in DOM.");
            return;
        }

        datasetList.innerHTML = "";

        links.forEach(link => {
            const datasetName = link.textContent;
            const datasetUrl = `http://localhost:8000/Map_JSON/${datasetName}`;
            console.log(`➕ Adding dataset: ${datasetName} (${datasetUrl})`);

            const button = document.createElement("button");
            button.textContent = datasetName;
            button.addEventListener("click", () => {
                console.log(`🖱️ Clicked: ${datasetName}`);
                loadDatasetForMap(datasetUrl, datasetName);
            });

            datasetList.appendChild(button);
        });

        console.log("✅ Dataset list updated in DOM.");

    } catch (error) {
        console.error("❌ Error fetching dataset list:", error);
    }
}


console.log("✅ Dataset list updated in DOM.");


// Function to dynamically load datasets
async function loadDataset(datasetUrl, key) {
    console.log(`🔍 loadDataset called with: URL=${datasetUrl}, Key=${key}`);

    try {
        const response = await fetch(datasetUrl);
        console.log(`📥 Response for ${key || "UNKNOWN KEY"}: Status ${response.status}`);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        console.log("✅ Successfully fetched dataset");

        const data = await response.json();

        // Ensure valid JSON format
        if (!Array.isArray(data) || data.length === 0) {
            console.error("❌ Invalid dataset format: Expected a non-empty array.");
            return;
        }

        console.log(`✅ Successfully loaded ${key} (${data.length} entries)`);
        console.log("🔍 First entry:", data[0]); // Log the first entry for debugging

        const controlsContainer = document.getElementById("data-controls");
        if (!controlsContainer) {
            console.error("❌ Element #data-controls not found in DOM.");
            return;
        }
        console.log("🛠️ Found #data-controls element");

        controlsContainer.innerHTML = ""; // Clear previous controls

        const headers = Object.keys(data[0]).filter(
            key => key !== "OA_Code" && key !== "Latitude" && key !== "Longitude"
        );
        console.log("📌 Extracted headers:", headers);

        const groupedHeaders = groupHeaders(headers);
        console.log("📂 Grouped headers:", Object.keys(groupedHeaders));

        // Generate UI for each category
        Object.entries(groupedHeaders).forEach(([category, datasets]) => {
            console.log(`📁 Creating category: ${category}`);

            const details = document.createElement("details");
            const summary = document.createElement("summary");
            summary.textContent = category;
            details.appendChild(summary);

            const dropdown = document.createElement("div");
            dropdown.classList.add("dropdown-content");

            datasets.forEach(dataset => {
                const datasetId = `toggle-${dataset.replace(/\s+/g, "-").toLowerCase()}`;

                console.log(`🔹 Adding dataset option: ${dataset}`);

                const label = document.createElement("label");
                const checkbox = document.createElement("input");

                checkbox.type = "checkbox";
                checkbox.id = datasetId;
                checkbox.setAttribute("data-dataset", dataset);
                checkbox.checked = false;

                checkbox.addEventListener("change", () => {
                    console.log(`🔀 Checkbox changed: ${dataset}, Checked: ${checkbox.checked}`);
                    checkbox.checked ? fetchDataset(dataset) : removeDataset(dataset);
                });

                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(dataset));

                const wrapper = document.createElement("div");
                wrapper.appendChild(label);
                dropdown.appendChild(wrapper);
            });

            details.appendChild(dropdown);
            controlsContainer.appendChild(details);
            console.log(`✅ Category added: ${category}`);
        });

    } catch (error) {
        console.error("❌ Error loading dataset:", error);
    }
}


// Function to group dataset headers
function groupHeaders(headers) {
    console.log("📌 Grouping headers:", headers);

    const groups = {};

    headers.forEach(header => {
        let category = "Other";
        const lowerHeader = header.toLowerCase(); // Store lowercase version once

        console.log(`🔍 Checking header: "${header}"`);

        if (lowerHeader.includes("all people")) {
            category = "All People";
        } else if (lowerHeader.includes("male") && !lowerHeader.includes("female")) {
            category = "Male Only";
        } else if (lowerHeader.includes("female") && !lowerHeader.includes("male")) {
            category = "Female Only";
        } else if (lowerHeader.includes("female")) {
            // Catch any remaining female-related headers
            category = "Female Only";
        }

        console.log(`📂 Assigned category for "${header}": ${category}`);

        if (!groups[category]) {
            groups[category] = [];
            console.log(`🆕 Created new category: ${category}`);
        }

        groups[category].push(header);
    });

    console.log("✅ Final grouped headers:", groups);
    return groups;
}


async function initializeMap() {
    console.log("🗺️ Initializing Map...");
    populateDatasetList();

    const map = L.map("map").setView([55.3781, -3.4360], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    const layerGroups = {};

    async function loadDatasetForMap(datasetUrl, key) {
        console.log(`📥 Fetching dataset: ${datasetUrl} for key: ${key}`);

        try {
            const response = await fetch(datasetUrl);
            console.log(`📥 Response for ${key}: Status ${response.status}`);

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const data = await response.json();
            console.log(`✅ Successfully loaded ${key} (${data.length} entries)`);

            if (!data || data.length === 0) {
                console.warn(`⚠️ Empty dataset received for ${key}`);
                return;
            }

            if (!layerGroups[key]) {
                console.log(`🆕 Creating new layer group for: ${key}`);
                layerGroups[key] = L.layerGroup();
            }

            data.forEach((entry) => {
                try {
                    console.log("🔹 Processing entry:", entry);
                    const lat = parseFloat(entry.Latitude);
                    const lon = parseFloat(entry.Longitude);

                    if (isNaN(lat) || isNaN(lon)) {
                        console.warn("❌ Skipping invalid lat/lon:", entry);
                        return;
                    }

                    const marker = L.circleMarker([lat, lon], {
                        radius: 5,
                        color: "blue",
                    });

                    marker.entry = entry;
                    marker.bindPopup(`OA Code: ${entry.OA_Code}`);

                    layerGroups[key].addLayer(marker);
                    console.log(`✅ Added marker for ${key}:`, marker);
                } catch (markerError) {
                    console.error(`❌ Error processing entry in ${key}:`, markerError);
                }
            });

            console.log(`🗂️ Layer Group Updated: ${key}`, layerGroups[key]);
        } catch (error) {
            console.error(`❌ Error loading dataset for ${key}:`, error);
        }
    }

    // Ensure datasets are dynamically loaded
    populateDatasetList();
}




// Functions to handle dataset toggling
function fetchDataset(dataset) {
    console.log("🔄 fetchDataset called with:", dataset);
    console.log(`Fetching dataset: ${dataset}`);
}

function removeDataset(dataset) {
    console.log("🗑️ removeDataset called with:", dataset);
    console.log(`Removing dataset: ${dataset}`);
}