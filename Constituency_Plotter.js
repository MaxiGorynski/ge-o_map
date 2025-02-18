window.constituencyData = []; // Store constituency boundaries globally

export async function loadAndPlotConstituencies() {
    console.log("📌 Starting to load constituency data...");

    if (!window.map) {
        console.error("❌ Error: `window.map` is not defined. Cannot add constituency layers.");
        return;
    }

    try {
        const response = await fetch("/westminster-parliamentary-constituencies.geojson");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log(`✅ Successfully loaded ${data.features.length} constituencies.`);

        if (!window.constituencyLayer) {
            console.log("ℹ️ Creating new constituencyLayer...");
            window.constituencyLayer = L.layerGroup().addTo(window.map);
        } else {
            console.log("♻️ Clearing previous constituency layers...");
            window.constituencyLayer.clearLayers();
        }

        // ✅ Store constituency polygons globally for reference
        window.constituencyData = data.features.map(feature => ({
            name: feature.properties.PCON22NM || "Unknown",
            geometry: feature.geometry
        }));

        let geoJsonFeatures = data.features.map(feature => ({
            type: "Feature",
            properties: { name: feature.properties.PCON22NM || "Unknown" },
            geometry: feature.geometry
        }));

        window.constituencyLayer = L.geoJSON(
            { type: "FeatureCollection", features: geoJsonFeatures },
            {
                style: {
                    color: "#00f2ff",
                    weight: 2,
                    fillOpacity: 0.2
                },
                onEachFeature: function (feature, layer) {
                    if (feature.properties && feature.properties.name) {
                        layer.bindPopup(`<b>Constituency:</b> ${feature.properties.name}`);
                    }
                }
            }
        ).addTo(window.map);

        window.constituencyLayer.bringToBack();
        console.log("✅ Constituency layer sent to back.");

    } catch (error) {
        console.error("❌ Error loading constituency data:", error);
    }
}
