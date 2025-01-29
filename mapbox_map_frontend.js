console.log("Mapbox GL JS script loaded");

map.on('load', () => {
    console.log("Map has loaded");
    loadAndDisplayDataset(datasetUrl);
});

async function loadAndDisplayDataset(url) {
    try {
        console.log("Loading dataset from", url);
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();

        console.log("Dataset loaded:", data);

        map.on('load', () => {
            console.log("Adding GeoJSON to map");
            map.addSource('dataset', {
                type: 'geojson',
                data: data
            });

            map.addLayer({
                id: 'dataset-points',
                type: 'circle',
                source: 'dataset',
                paint: {
                    'circle-radius': 6,
                    'circle-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'scalar'],
                        0, '#2DC4B2',
                        50, '#3BB3C3',
                        100, '#669EC4'
                    ]
                }
            });
        });
    } catch (error) {
        console.error("Error loading dataset:", error);
    }
}
