from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/datasets/dataset1.geojson')
def get_dataset1():
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-3.1883, 55.9533]
                },
                "properties": {
                    "scalar": 45
                }
            }
        ]
    }
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
