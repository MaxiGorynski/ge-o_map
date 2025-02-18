let map;
const layerGroups = {}; // Store dataset layers

// ✅ Import Constituency Plotter Module
import { loadAndPlotConstituencies } from "./Constituency_Plotter.js";

// ✅ Define EPSG:27700 (British National Grid)
proj4.defs("EPSG:27700", "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +datum=OSGB36 +units=m +no_defs");

// ✅ Define WGS84 (Standard Lat/Lon format)
proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");

console.log("✅ Proj4 definitions loaded for EPSG:27700 and EPSG:4326");

//1️⃣ Initialise the map (Runs once)
async function initialiseMap() {
    console.log("🗺️ Initialising Map...");

    // ✅ Attach map to the `window` object to ensure global access
    window.map = L.map("map").setView([55.3781, -3.4360], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
    }).addTo(window.map);

    console.log("✅ Global map object (from script.js):", window.map);


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
        let links = [...htmlDoc.querySelectorAll("a[href$='.json']")];
        console.log(`🔗 Found ${links.length} dataset links.`);

        const datasetList = document.getElementById("dataset-list");
        if (!datasetList) {
            console.error("❌ Element #dataset-list not found in DOM.");
            return;
        }

        datasetList.innerHTML = ""; // Clear previous entries

        // Sort numerically instead of lexicographically
        links.sort((a, b) => {
            const numA = parseInt(a.textContent.match(/\d+/) || "0", 10);
            const numB = parseInt(b.textContent.match(/\d+/) || "0", 10);
            return numA - numB;
        });

        links.forEach(link => {
            const datasetName = link.textContent; // Keep original filename for URL
            const datasetUrl = `http://localhost:8000/Map_JSON/${datasetName}`; // URL must match the file

            const displayName = datasetName.replace(".json", "").replace(/_/g, " "); // Cleaned name
            console.log(`➕ Adding dataset: ${displayName} (${datasetUrl})`);

            const button = document.createElement("button");
            button.textContent = displayName;
            button.dataset.dataset = datasetName; // Store dataset key in button attribute
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
        console.log("🔍 First entry:", data[0]);

        const datasetButton = document.querySelector(`button[data-dataset="${key}"]`);
        if (!datasetButton) {
            console.error(`❌ Button for dataset ${key} not found.`);
            return;
        }

        // 🔥 Remove any existing dropdowns for this dataset
        const existingDropdown = datasetButton.nextElementSibling;
        if (existingDropdown && existingDropdown.classList.contains("dropdown-container")) {
            existingDropdown.remove();
            return; // If dropdown exists, remove it and return
        }

        // 🔥 Extract and group dataset headers
        const headers = Object.keys(data[0]).filter(
            key => key !== "OA_Code" && key !== "Latitude" && key !== "Longitude"
        );

        const groupedHeaders = groupHeaders(headers);
        console.log("📂 Grouped headers:", Object.keys(groupedHeaders));

        // 🔥 Create a dropdown container
        const dropdownContainer = document.createElement("div");
        dropdownContainer.classList.add("dropdown-container");

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
                    console.log("   🔍 Checking dataset keys:", Object.keys(layerGroups));

                    if (checkbox.checked) {
                        console.log(`🟢 Adding dataset: ${dataset}`);
                        addLayerToMap(dataset, data);
                    } else {
                        console.log(`🔴 Removing dataset: ${dataset}`);
                        removeLayerFromMap(dataset);
                    }
                });

                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(` ${dataset}`));

                dropdown.appendChild(label);
                dropdown.appendChild(document.createElement("br"));
            });

            details.appendChild(dropdown);
            dropdownContainer.appendChild(details);
        });

        // ✅ Insert dropdown **right below** the clicked dataset button
        datasetButton.insertAdjacentElement("afterend", dropdownContainer);

        console.log(`✅ Dropdown inserted for ${key}`);

    } catch (error) {
        console.error("❌ Error loading dataset:", error);
    }
}

const markerMap = {}; // 🏷️ Global object to store markers by OA_Code

async function loadOAConstituencyMapping() {
    console.log("📌 Loading OA → Constituency mappings...");

    try {
        const response = await fetch("/final_oa_constituency_mapping.csv"); // Adjust path if needed
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const csvText = await response.text();
        const rows = csvText.split("\n").slice(1); // Skip header

        window.oaConstituencyMap = {}; // Global storage for quick lookups

        rows.forEach(row => {
            const [oaCode, lat, lon, constituency] = row.split(",");
            if (oaCode) {
                window.oaConstituencyMap[oaCode] = constituency?.trim() || "Unknown";
            }
        });

        console.log(`✅ Loaded ${Object.keys(window.oaConstituencyMap).length} OA → Constituency mappings.`);
    } catch (error) {
        console.error("❌ Error loading OA → Constituency mapping:", error);
    }
}

// ✅ Ensure OA constituency mapping is loaded before using addLayerToMap()
if (!window.oaConstituencyMap) {
    loadOAConstituencyMapping();
}

async function addLayerToMap(dataset, data) {
    console.log(`📌 Adding layer for ${dataset}`);

    if (!window.map) {
        console.error("❌ ERROR: `window.map` is not defined. Cannot proceed.");
        return;
    }

    if (!window.layerGroups) window.layerGroups = {};
    if (!window.markerMap) window.markerMap = {};

    if (!window.layerGroups[dataset]) {
        console.warn(`⚠️ layerGroups[${dataset}] was undefined. Initializing...`);
        window.layerGroups[dataset] = L.layerGroup().addTo(window.map);
    } else {
        console.log(`♻️ Clearing existing dataset layer: ${dataset}`);
        window.layerGroups[dataset].clearLayers();
    }

    // ✅ Verify OA → Constituency Mapping is available
    if (!window.oaConstituencyMap) {
        console.error("❌ ERROR: `window.oaConstituencyMap` is not loaded. Cannot assign constituencies.");
        return;
    }

    console.log(`🗂️ Current layerGroups:`, Object.keys(window.layerGroups));

    const values = data
        .map(entry => parseFloat(entry[dataset]))
        .filter(value => !isNaN(value))
        .sort((a, b) => a - b);

    if (values.length === 0) {
        console.warn("⚠️ No valid numerical values found for dataset:", dataset);
        return;
    }

    const minValue = values[0];
    const maxValue = values[values.length - 1];
    const top5Index = Math.max(0, Math.floor(values.length * 0.95) - 1);
    const top5Threshold = values[top5Index] || maxValue;

    console.log(`📊 Min: ${minValue}, Max: ${maxValue}, 95th Percentile Threshold: ${top5Threshold}`);

    data.forEach(entry => {
        try {
            const lat = parseFloat(entry.Latitude);
            const lon = parseFloat(entry.Longitude);
            const datasetValue = entry.hasOwnProperty(dataset) ? parseFloat(entry[dataset]) || 0 : 0;

            if (isNaN(lat) || isNaN(lon)) {
                console.warn("❌ Skipping invalid lat/lon:", entry);
                return;
            }

            const constituencyName = window.oaConstituencyMap[entry.OA_Code] || "Unknown";

            if (!window.markerMap[entry.OA_Code]) {
                const marker = L.circleMarker([lat, lon], {
                    radius: 5,
                    color: getMagentaColour((datasetValue - minValue) / (maxValue - minValue || 1)),
                    fillColor: getMagentaColour((datasetValue - minValue) / (maxValue - minValue || 1)),
                    fillOpacity: 0.8
                });

                marker.entry = entry;
                marker.datasetValues = {};
                window.markerMap[entry.OA_Code] = marker;

                marker.bindPopup(`
                    <b>OA Code:</b> ${entry.OA_Code} <br>
                    <b>Constituency:</b> ${constituencyName} <br>
                    ${Object.entries(marker.datasetValues)
                        .map(([key, value]) => `<b>${key}:</b> ${value}`)
                        .join("<br>")}
                `);

                window.layerGroups[dataset].addLayer(marker);
            }

            // ✅ Corrected: Use existing marker, not redeclare it
            const marker = window.markerMap[entry.OA_Code];
            marker.datasetValues[dataset] = datasetValue;

        } catch (markerError) {
            console.error(`❌ ERROR processing entry in ${dataset}:`, markerError, entry);
        }
    });

    console.log(`🗂️ Layer Group Updated: ${dataset}`, window.layerGroups[dataset]);

}


const flagMarkers = {}; // Global storage for high-value flags

// 🚩 Function to place a "High" flag on high-value markers
function placeHighValueFlag(lat, lon, dataset) {
    console.log(`🚩 Placing "High" flag for ${dataset} at: (${lat}, ${lon})`);

    // Slightly offset the flag so it doesn't overlap with the marker
    const offsetLat = lat + 0.0008;
    const offsetLon = lon + 0.0008;

    const flag = L.marker([offsetLat, offsetLon], {
        icon: L.icon({
            iconUrl: '/static/green_flag.png',
            iconSize: [15, 15],
            iconAnchor: [15, 30],
            popupAnchor: [0, -30]
        })
    });

    // ✅ Ensure `window.flagMarkers` exists
    if (!window.flagMarkers) {
        window.flagMarkers = {};
    }

    // ✅ Ensure `window.flagMarkers[dataset]` exists
    if (!window.flagMarkers[dataset]) {
        window.flagMarkers[dataset] = [];
    }

    // ✅ Store flag for later removal
    window.flagMarkers[dataset].push(flag);
    flag.addTo(window.map);
}

// 🎨 Function to generate a magenta colour gradient from light magenta (low values) to dark magenta (high values)
function getMagentaColour(value) {
    const startColor = [255, 182, 193]; // Light magenta (light pink) for low values
    const endColor = [139, 0, 139]; // Dark magenta for high values

    const r = Math.round(startColor[0] + (endColor[0] - startColor[0]) * value);
    const g = Math.round(startColor[1] + (endColor[1] - startColor[1]) * value);
    const b = Math.round(startColor[2] + (endColor[2] - startColor[2]) * value);

    return `rgb(${r}, ${g}, ${b})`;
}

// 🚨 Function to clear ALL layers from the map safely, including data markers
function clearAllLayers() {
    console.log("🗑️ Clearing ALL layers!");

    // ✅ Step 1: Remove all dataset layers
    if (window.layerGroups) {
        Object.keys(window.layerGroups).forEach(dataset => {
            if (window.layerGroups[dataset]) {
                try {
                    window.map.removeLayer(window.layerGroups[dataset]);
                } catch (error) {
                    console.error(`❌ Error removing dataset layer "${dataset}":`, error);
                }
                delete window.layerGroups[dataset];
            }
        });
    } else {
        console.warn("⚠️ No layer groups found to remove.");
    }

    // ✅ Step 2: Remove all constituency boundaries
    if (window.constituencyLayer) {
        console.log("🗺️ Removing constituency boundaries...");
        try {
            window.map.removeLayer(window.constituencyLayer);
        } catch (error) {
            console.error("❌ Error removing constituency boundaries:", error);
        }
        delete window.constituencyLayer;
    } else {
        console.warn("⚠️ No constituency boundaries found to remove.");
    }

    // ✅ Step 3: Remove all markers from `markerMap`
    if (window.markerMap) {
        Object.keys(window.markerMap).forEach(oaCode => {
            try {
                window.map.removeLayer(window.markerMap[oaCode]);
            } catch (error) {
                console.error(`❌ Error removing marker "${oaCode}":`, error);
            }
            delete window.markerMap[oaCode];
        });
    } else {
        console.warn("⚠️ No data markers found to remove.");
    }

    // ✅ Step 4: Remove all flags
    if (window.flagMarkers) {
        Object.keys(window.flagMarkers).forEach(dataset => {
            window.flagMarkers[dataset].forEach(flag => {
                try {
                    window.map.removeLayer(flag);
                } catch (error) {
                    console.error("❌ Error removing flag:", error);
                }
            });
        });
        window.flagMarkers = {}; // Reset flags
        console.log("🚨 All flags removed.");
    } else {
        console.warn("⚠️ No flags found to remove.");
    }

    // ✅ Step 5: Reset all checkboxes **including dynamically created ones**
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    console.log(`🔄 Found ${checkboxes.length} checkboxes to reset.`);

    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        console.log(`⬜ Checkbox ${checkbox.dataset.dataset} unchecked.`);
    });

    console.log("🔄 All checkboxes reset to unchecked.");
    console.log("🧹 All layers, markers, constituency boundaries, and checkboxes successfully cleared!");
}

// 🚨 Function to remove all high-value flags when no datasets remain
function clearAllFlags() {
    console.log("🚨 Clearing ALL high-value flags...");

    Object.values(window.flagMarkers).forEach(datasetFlags => {
        datasetFlags.forEach(flag => {
            try {
                window.map.removeLayer(flag);
            } catch (error) {
                console.error("❌ Failed to remove flag:", error);
            }
        });
    });

    // ✅ Explicitly reset `flagMarkers`
    window.flagMarkers = {};
    console.log("✅ All high-value flags removed.");
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

function removeLayerFromMap(dataset) {
    console.log(`🗑️ Removing layer for ${dataset}`);

    // ✅ Ensure `window.layerGroups` exists
    if (!window.layerGroups || Object.keys(window.layerGroups).length === 0) {
        console.warn("⚠️ No layer groups found. Nothing to remove.");
        return;
    }

    console.log(`🔍 Existing layerGroups before removal:`, Object.keys(window.layerGroups));

    // ✅ Remove the dataset layer if it exists
    if (window.layerGroups[dataset]) {
        window.map.removeLayer(window.layerGroups[dataset]);
        delete window.layerGroups[dataset];
    } else {
        console.warn(`⚠️ No layer found for ${dataset}`);
    }

    // ✅ Remove dataset markers from `markerMap`
    Object.keys(window.markerMap).forEach(oaCode => {
        if (window.markerMap[oaCode] && window.markerMap[oaCode].datasetValues[dataset]) {
            try {
                window.map.removeLayer(window.markerMap[oaCode]);
            } catch (error) {
                console.error(`❌ Failed to remove marker: ${oaCode}`, error);
            }
            delete window.markerMap[oaCode].datasetValues[dataset];
        }
    });

    // ✅ Remove all flags for this dataset
    if (window.flagMarkers && window.flagMarkers[dataset]) {
        console.log(`🚨 Removing ${window.flagMarkers[dataset].length} flags for dataset: ${dataset}`);

        window.flagMarkers[dataset].forEach(flag => {
            try {
                window.map.removeLayer(flag);
            } catch (error) {
                console.error(`❌ Failed to remove flag for ${dataset}`, error);
            }
        });

        // ✅ Explicitly delete the dataset entry in `flagMarkers`
        delete window.flagMarkers[dataset];
    }

    // ✅ 🔥 If NO datasets remain, remove **all** remaining flags
    if (Object.keys(window.layerGroups).length === 0) {
        console.log("🚨 No datasets left, clearing all remaining flags...");
        clearAllFlags();
    }

    console.log(`🔍 Remaining layerGroups after:`, Object.keys(window.layerGroups));
    console.log(`🗂️ Finished removing dataset: ${dataset}`);
}


// 7️⃣ Run everything in the correct order when the page loads
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📌 DOM fully loaded. Initializing...");

    // ✅ Check if Proj4 and Leaflet are loaded before proceeding
    if (typeof proj4 === "undefined" || typeof L === "undefined") {
        console.error("❌ Leaflet and Proj4 must be loaded first! Retrying in 1 second...");
        setTimeout(() => location.reload(), 1000); // Retry after 1 sec
        return;
    }

    console.log("✅ Proj4 definitions loaded for EPSG:27700 and EPSG:4326");
    // Ensure the Clear Layers button exists before adding the event listener
    const clearLayersBtn = document.getElementById("clear-layers-btn");
    if (clearLayersBtn) {
        clearLayersBtn.addEventListener("click", clearAllLayers);
        console.log("🧹 Clear All Layers button event listener added.");
    } else {
        console.error("❌ Clear All Layers button not found in DOM.");
    }

    try {
        const { loadAndPlotConstituencies } = await import("./constituency_plotter.js");

        // ✅ Ensure toggle button exists
        const toggleConstituenciesBtn = document.getElementById("const-view-btn");
        if (toggleConstituenciesBtn) {
            toggleConstituenciesBtn.addEventListener("click", async () => {
                console.log("🗺️ Toggling constituencies...");
                await loadAndPlotConstituencies();
            });
        } else {
            console.error("❌ Toggle Constituencies button not found in DOM.");
        }
    } catch (error) {
        console.error("❌ Error importing constituency_plotter.js:", error);
    }

    initialiseMap();  // 🌍 Step 1: Start the map
    console.log("✅ Checking if `window.map` exists in Constituency_Plotter.js:", window.map);
    await populateDatasetList();  // 📋 Step 2: Populate dataset list

});
