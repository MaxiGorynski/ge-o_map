export async function loadAndPlotConstituencies() {
    console.log("📌 Loading constituency data...");

    try {
        const response = await fetch("/westminster-parliamentary-constituencies.geojson");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log(`✅ Loaded ${data.features.length} constituencies.`);

        // 🏗️ Ensure global constituencyLayer exists
        if (!window.constituencyLayer) {
            window.constituencyLayer = L.layerGroup(); // ✅ Initialize if missing
        } else {
            window.constituencyLayer.clearLayers(); // ✅ Remove old layers if they exist
        }

        let validFeatures = 0;

        data.features.forEach((feature, index) => {
            const { geometry, properties } = feature;

            // ✅ Skip invalid geometries
            if (!geometry || !geometry.coordinates) {
                console.warn(`⚠️ Skipping invalid geometry at index ${index}:`, feature);
                return;
            }

            if (geometry.type === "Polygon") {
                // ✅ Ensure each coordinate is an array before transformation
                let correctedCoordinates = geometry.coordinates.map(ring => {
                    if (!Array.isArray(ring)) {
                        console.warn(`⚠️ Unexpected coordinate format in Polygon at index ${index}:`, ring);
                        return [];
                    }
                    return ring.map(([lon, lat]) => [lat, lon]); // Swap [lon, lat] → [lat, lon]
                });

                // ✅ Create a Leaflet polygon
                const polygon = L.polygon(correctedCoordinates, {
                    color: "red",
                    weight: 2,
                    fillOpacity: 0.3
                });

                if (!polygon) {
                    console.error(`❌ Failed to create a polygon at index ${index}`);
                    return;
                }

                polygon.bindPopup(`<b>Constituency:</b> ${properties.PCON22NM || "Unknown"}`);
                window.constituencyLayer.addLayer(polygon);
                validFeatures++;
            } else if (geometry.type === "MultiPolygon") {
                // ✅ Ensure MultiPolygon handling is correct
                let correctedCoordinates = geometry.coordinates.map(polygon =>
                    polygon.map(ring => {
                        if (!Array.isArray(ring)) {
                            console.warn(`⚠️ Unexpected coordinate format in MultiPolygon at index ${index}:`, ring);
                            return [];
                        }
                        return ring.map(([lon, lat]) => [lat, lon]);
                    })
                );

                const multiPolygon = L.polygon(correctedCoordinates, {
                    color: "blue",
                    weight: 2,
                    fillOpacity: 0.3
                });

                if (!multiPolygon) {
                    console.error(`❌ Failed to create a multipolygon at index ${index}`);
                    return;
                }

                multiPolygon.bindPopup(`<b>Constituency:</b> ${properties.PCON22NM || "Unknown"}`);
                window.constituencyLayer.addLayer(multiPolygon);
                validFeatures++;
            } else {
                console.warn(`⚠️ Unexpected geometry type (${geometry.type}) at index ${index}:`, feature);
            }
        });

        // ✅ Only add to map if there are valid features
        if (validFeatures > 0) {
            console.log(`✅ Successfully plotted ${validFeatures} constituencies.`);
            window.constituencyLayer.addTo(map);
        } else {
            console.warn("⚠️ No valid constituency boundaries found.");
        }

    } catch (error) {
        console.error("❌ Error loading constituency data:", error);
    }
}
