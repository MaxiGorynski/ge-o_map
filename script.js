let map;
const layerGroups = {}; // Store dataset layers

//1️⃣ Initialise the map (Runs once)
async function initialiseMap() {
    console.log("🗺️ Initialising Map...");

    map = L.map("map").setView([55.3781, -3.4360], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    console.log("✅ Map initialised.");
}

// 2️⃣ Populate dataset list in the UI
async function populateDatasetList() {
    console.log("✅ populateDatasetList called");
    console.log("📥 Fetching dataset list from server...");

    try {
        const response = await fetch("http://localhost:8000/Map_JSON/");
        console.log("📥 Response received for dataset list:", response);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const parser = new DOMParser();
        const htmlText = await response.text();
        console.log("📄 Raw HTML fetched:", htmlText.substring(0, 500));

        const htmlDoc = parser.parseFromString(htmlText, "text/html");
        const links = [...htmlDoc.querySelectorAll("a[href$='.json']")];
        console.log(`🔗 Found ${links.length} dataset links.`);

        const datasetList = document.getElementById("dataset-list");
        if (!datasetList) {
            console.error("❌ Element #dataset-list not found in DOM.");
            return;
        }

        datasetList.innerHTML = ""; // Clear previous entries

        links.forEach(link => {
            const datasetName = link.textContent; // Keep original filename for URL
            const datasetUrl = `http://localhost:8000/Map_JSON/${datasetName}`; // URL must match the file

            const displayName = datasetName.replace(".json", "").replace(/_/g, " "); // Cleaned name
            console.log(`➕ Adding dataset: ${displayName} (${datasetUrl})`);

            const button = document.createElement("button");
            button.textContent = displayName;
            button.style.textAlign = "left"; // Align button text to the left
            button.style.display = "block"; // Ensure buttons stack vertically
            button.style.width = "100%"; // Make buttons full width
            button.style.marginBottom = "5px"; // Add spacing between buttons

            button.addEventListener("click", () => {
                console.log(`🖱️ Clicked: ${datasetName}`);
                loadDataset(datasetUrl, datasetName); // Ensure proper dataset loading
            });

            datasetList.appendChild(button);
        });

        console.log("✅ Dataset list updated in DOM.");
    } catch (error) {
        console.error("❌ Error fetching dataset list:", error);
    }
}



// 3️⃣ Load dataset & show headers in a dropdown
async function loadDataset(datasetUrl, key) {
    console.log(`📂 Attempting to load dataset: ${datasetUrl}`);

    try {
        const response = await fetch(datasetUrl);
        console.log(`📥 Response for ${key}: Status ${response.status}`);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        console.log("✅ Successfully fetched dataset");

        const data = await response.json();
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

        controlsContainer.innerHTML = ""; // Clear previous controls

        // 🔥 Extract and group dataset headers
        const headers = Object.keys(data[0]).filter(
            key => key !== "OA_Code" && key !== "Latitude" && key !== "Longitude"
        );

        const groupedHeaders = groupHeaders(headers);
        console.log("📂 Grouped headers:", Object.keys(groupedHeaders));

        // 🔥 Create checkboxes for datasets with line breaks
        Object.entries(groupedHeaders).forEach(([category, datasets]) => {
            console.log(`📁 Creating category: ${category}`);

            const details = document.createElement("details");
            const summary = document.createElement("summary");
            summary.textContent = category;
            details.appendChild(summary);

            const dropdown = document.createElement("div");
            dropdown.classList.add("dropdown-content");

            datasets.forEach(dataset => {
                console.log(`🔹 Adding dataset option: ${dataset}`);

                const label = document.createElement("label");
                const checkbox = document.createElement("input");

                checkbox.type = "checkbox";
                checkbox.setAttribute("data-dataset", dataset);
                checkbox.checked = false;

                checkbox.addEventListener("change", () => {
                    console.log(`🔀 Checkbox changed: ${dataset}, Checked: ${checkbox.checked}`);
                    checkbox.checked ? addLayerToMap(dataset, data) : removeLayerFromMap(dataset);
                });

                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(` ${dataset}`));

                // ✅ Append to dropdown with a line break
                dropdown.appendChild(label);
                dropdown.appendChild(document.createElement("br"));
            });

            details.appendChild(dropdown);
            controlsContainer.appendChild(details);
            console.log(`✅ Category added: ${category}`);
        });

    } catch (error) {
        console.error("❌ Error loading dataset:", error);
    }
}


// 4️⃣ Add selected dataset layer to the map
function addLayerToMap(dataset, data) {
    console.log(`📌 Adding layer for ${dataset}`);

    if (!layerGroups[dataset]) {
        console.log(`🆕 Creating new layer group for: ${dataset}`);
        layerGroups[dataset] = L.layerGroup();
    }

    data.forEach(entry => {
        try {
            const lat = parseFloat(entry.Latitude);
            const lon = parseFloat(entry.Longitude);

            if (isNaN(lat) || isNaN(lon)) {
                console.warn("❌ Skipping invalid lat/lon:", entry);
                return;
            }

            const datasetValue = entry[dataset] ?? "N/A"; // Fetch dataset value or default to 'N/A'

            const marker = L.circleMarker([lat, lon], {
                radius: 5,
                color: "blue",
            });

            marker.entry = entry;
            marker.bindPopup(`
                <b>OA Code:</b> ${entry.OA_Code} <br>
                <b>${dataset}:</b> ${datasetValue}
            `);

            layerGroups[dataset].addLayer(marker);
        } catch (markerError) {
            console.error(`❌ Error processing entry in ${dataset}:`, markerError);
        }
    });

    console.log(`🗂️ Layer Group Updated: ${dataset}`, layerGroups[dataset]);
    map.addLayer(layerGroups[dataset]);
}


// 5️⃣ Remove dataset layer from the map
function removeLayerFromMap(dataset) {
    console.log(`🗑️ Removing layer for ${dataset}`);

    if (layerGroups[dataset]) {
        map.removeLayer(layerGroups[dataset]);
        delete layerGroups[dataset];
    }
}

// 6️⃣ Group headers (for dropdown categories)
function groupHeaders(headers) {
    console.log("📌 Grouping headers:", headers);

    const groups = {};

    headers.forEach(header => {
        let category;
        const lowerHeader = header.toLowerCase();

        console.log(`🔍 Checking header: "${header}"`);

        // Extract category name before the first comma, or keep the full name if no comma exists
        category = header.includes(",") ? header.split(",")[0].trim() : header.trim();

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



// 7️⃣ Run everything in the correct order when the page loads
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📌 DOM fully loaded. Initialising...");
    initialiseMap();  // 🌍 Step 1: Start the map
    await populateDatasetList();  // 📋 Step 2: Populate dataset list
});
