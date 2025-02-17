export async function loadAndPlotConstituencies() {
    console.log("📌 Starting to load constituency data...");

    if (!window.map) {
        console.error("❌ Error: `window.map` is not defined. Cannot add constituency layers.");
        return;
    }

    try {
        // ✅ Fetch the GeoJSON data
        const response = await fetch("/westminster-parliamentary-constituencies.geojson");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log(`✅ Successfully loaded ${data.features.length} constituencies.`);

        // ✅ Step 1: Ensure global constituencyLayer is properly initialized
        if (!window.constituencyLayer) {
            console.log("ℹ️ Creating new constituencyLayer...");
            window.constituencyLayer = L.layerGroup().addTo(window.map);
        } else {
            console.log("♻️ Clearing previous constituency layers...");
            window.constituencyLayer.clearLayers();
        }

        let validFeatures = 0;
        let geoJsonFeatures = [];

        // ✅ Step 2: Iterate through each feature and validate
        data.features.forEach((feature, index) => {
            const { geometry, properties } = feature;

            console.log(`🔍 Processing feature #${index + 1}:`, properties?.PCON22NM || "Unknown");

            if (!geometry || !geometry.coordinates) {
                console.warn(`⚠️ Skipping invalid geometry at index ${index}:`, feature);
                return;
            }

            if (geometry.type !== "Polygon" && geometry.type !== "MultiPolygon") {
                console.warn(`⚠️ Unexpected geometry type (${geometry.type}) at index ${index}:`, feature);
                return;
            }

            geoJsonFeatures.push(feature);
            validFeatures++;
        });

        // ✅ Step 3: Ensure we have valid data before creating the layer
        if (validFeatures > 0) {
            console.log(`✅ Preparing to plot ${validFeatures} valid constituency polygons...`);

            window.constituencyLayer = L.geoJSON(
                { type: "FeatureCollection", features: geoJsonFeatures },
                {
                    style: {
                        color: "#00f2ff",
                        weight: 2,
                        fillOpacity: 0.2
                    },
                    onEachFeature: function (feature, layer) {
                        if (feature.properties && feature.properties.PCON22NM) {
                            layer.bindPopup(`<b>Constituency:</b> ${feature.properties.PCON22NM}`);
                        }
                    }
                }
            ).addTo(window.map);

            // ✅ Ensure constituency layer stays behind markers
            window.constituencyLayer.bringToBack();
            console.log("✅ Constituency layer sent to back.");


            // ✅ Add to `window.constituencyLayer` instead of overwriting it
            window.constituencyLayer.addLayer(constituencyGeoJsonLayer);

            console.log("✅ Successfully plotted all constituencies.");
        } else {
            console.warn("⚠️ No valid constituency boundaries found.");
        }

    } catch (error) {
        console.error("❌ Error loading constituency data:", error);
    }
}
