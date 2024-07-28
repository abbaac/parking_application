from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

def get_occupancy_data():
    try:
        with open('occupancy_data.json', 'r') as file:
            occupancy_data = json.load(file)
        return occupancy_data
    except Exception as e:
        return None

@app.route('/')
def index():
    occupancy_data = get_occupancy_data()
    if occupancy_data:
        if (occupancy_data['total_spaces'] == 0 and
            occupancy_data['free_spaces'] == 0 and
            occupancy_data['occupied_spaces'] == 0 and
            occupancy_data['available_spots'] == 0):
            return render_template('no_data.html')
        else:
            return render_template('index.html')
    else:
        return render_template('no_data.html')

@app.route('/occupancy', methods=['GET'])
def get_occupancy():
    occupancy_data = get_occupancy_data()
    if occupancy_data:
        response = {
            'status': 'success',
            'data': occupancy_data
        }
    else:
        response = {
            'status': 'error',
            'message': 'Could not load occupancy data'
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
