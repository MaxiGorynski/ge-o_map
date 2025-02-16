async function loadAndPlotConstituencies() {
    console.log("📌 Loading constituency data...");

    try {
        const response = await fetch("/westminster-parliamentary-constituencies.geojson");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log(`✅ Loaded ${data.features.length} constituencies.`);

        // 🏗️ Create a layer group to hold the constituency boundaries
        const constituencyLayer = L.layerGroup();

        data.features.forEach(feature => {
            const { geometry, properties } = feature;

            if (!geometry || geometry.type !== "Polygon") {
                console.warn("⚠️ Skipping invalid geometry:", feature);
                return;
            }

            // ✅ Create a GeoJSON Layer for each feature
            const polygon = L.geoJSON(feature, {
                style: {
                    color: "red",
                    weight: 2,
                    fillOpacity: 0.2
                }
            });

            // ✅ Bind a popup with the constituency name
            polygon.bindPopup(`<b>Constituency:</b> ${properties.PCON22NM || "Unknown"}`);

            // ✅ Add to the layer group
            constituencyLayer.addLayer(polygon);
        });

        // ✅ Finally, add the complete layer group to the map
        constituencyLayer.addTo(map);
        console.log("✅ Constituency data successfully added to the map.");

    } catch (error) {
        console.error("❌ Error loading constituency data:", error);
    }
}

export { loadAndPlotConstituencies };
