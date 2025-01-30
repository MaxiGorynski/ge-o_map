//Load JSON and generate UI dynamically based on JSON

async function loadDataset(jsonFile) {
    try {
        const response = await fetch(jsonFile);
        const data = await response.json();

        //Clear existing dataset controls
        const controlsContainer = document.getElementById("dataset-controls");
        controlsContainer.innerHTML = ""; // Reset UI

        //Extract headers/keys from JSON object
        const headers = Object.keys(data[0].filter(key => key !== "oa_code" && key !== "latitude" && key !== "longitude");

        //Group headers by category
        const groupedHeaders = groupedHeaders(headers)

        //Generate dropdowns dynamically
        Object.keys(groupedHeaders).forEach(category => {
            const details = document.createElement("details");
            const summary = document.createElement("summary");
            summary.textContent = category; // Set category name
            details.appendChild(summary);

            const dropdown = document.createElement("div");
            dropdown.classList.add("dropdown-content");

            //Create checkboxes for each dataset
            groupedHeaders[category].forEach(dataset => {
                const label = document.createElement("label");
                const checkbox = document.createElement("input");

                checkbox.type = "checkbox";
                checkbox.id = `toggle-${dataset.replace(/\s+/g, "-").toLowerCase()}`;
                checkbox.setAttribute("data-dataset", dataset);
                checkbox.checked = true;

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

//Function for grouping headers by category
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

//Load default dataset on page load
document.addEventListener("DOMContentLoaded", () => {
    loadDataset("default_dataset.json");
});

// Initialize the map
        const map = L.map('map').setView([55.3781, -3.4360], 6);

        // Add a tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Load the JSON data
        fetch('map_data.json')
            .then(response => response.json())
            .then(data => {
                console.log("Loaded data:", data);
                // Create feature groups
                const allPeopleGroup = L.layerGroup();
                const people0To4Group = L.layerGroup();
                const people5To9Group = L.layerGroup();
                const maleGroup = L.layerGroup();

                // Add markers to the feature groups
                data.forEach(item => {
                    console.log("Processing item:", item);
                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'blue',
                        fillColor: 'blue',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>Number of People:</strong> ${item.all_people}
                    `).addTo(allPeopleGroup);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'cyan',
                        fillColor: 'cyan',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>All People (0-4):</strong> ${item.all_people_0_4}
                    `).addTo(people0To4Group);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'purple',
                        fillColor: 'purple',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>All People (5-9):</strong> ${item.all_people_5_9}
                    `).addTo(people5To9Group);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'green',
                        fillColor: 'green',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>Male, All:</strong> ${item.male_all}
                    `).addTo(maleGroup);
                })
                .catch(error => console.error("Error loading data:", error));

                // All datasets in one list
                const layers = {
                    "Number of People (All)": allPeopleGroup,
                    "All People (0-4)": people0To4Group,
                    "All People (5-9)": people5To9Group,
                    "Male, All": maleGroup
                };

                // Populate the control panel
                const layerControl = document.getElementById('layerControl');
                Object.keys(layers).forEach(name => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = true; // Default to checked
                    checkbox.onchange = () => {
                        if (checkbox.checked) {
                            map.addLayer(layers[name]);
                        } else {
                            map.removeLayer(layers[name]);
                        }
                    };

                    const label = document.createElement('label');
                    label.appendChild(checkbox);
                    label.appendChild(document.createTextNode(name));

                    layerControl.appendChild(label);
                });

                // Add all layers initially
                Object.values(layers).forEach(layer => map.addLayer(layer));
            })
            .catch(error => console.error("Error loading data:", error));

        // Add a tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Load the JSON data
        fetch('map_data.json')
            .then(response => response.json())
            .then(data => {
                // Create feature groups for the map layers
                const layers = {
                    all_people: L.layerGroup(),
                    all_people_0_4: L.layerGroup(),
                    all_people_5_9: L.layerGroup(),
                    male_all: L.layerGroup()
                };

                // Populate each layer group with data
                data.forEach(item => {
                    console.log("Processing item:", item);
                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'blue',
                        fillColor: 'blue',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>Number of People:</strong> ${item.all_people}
                    `).addTo(layers.all_people);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'cyan',
                        fillColor: 'cyan',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>All People (0-4):</strong> ${item.all_people_0_4}
                    `).addTo(layers.all_people_0_4);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'purple',
                        fillColor: 'purple',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>All People (5-9):</strong> ${item.all_people_5_9}
                    `).addTo(layers.all_people_5_9);

                    L.circleMarker([item.latitude, item.longitude], {
                        radius: 5,
                        color: 'green',
                        fillColor: 'green',
                        fillOpacity: 0.7
                    }).bindPopup(`
                        <strong>OA Code:</strong> ${item.oa_code}<br>
                        <strong>Male, All:</strong> ${item.male_all}
                    `).addTo(layers.male_all);
                });

                // Handle dropdown toggle interactions
                const toggles = document.querySelectorAll("input[type='checkbox']");
                toggles.forEach(toggle => {
                    toggle.addEventListener("change", function () {
                        const dataset = toggle.dataset.dataset;
                        if (this.checked) {
                            map.addLayer(layers[dataset]);
                        } else {
                            map.removeLayer(layers[dataset]);
                        }
                    });
                });

                // Initially add all layers to the map
                Object.values(layers).forEach(layer => map.addLayer(layer));
            })
            .catch(error => console.error("Error loading data:", error));



        function fetchDataset(dataset) {
            console.log(`Fetching dataset: ${dataset}`);
            // Replace with API call or dataset rendering logic
        }

        function removeDataset(dataset) {
            console.log(`Removing dataset: ${dataset}`);
            // Replace with map-clearing logic
        }

