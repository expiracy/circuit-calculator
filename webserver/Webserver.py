import json
from os.path import join, dirname, realpath
from circuit.CircuitManager import CircuitManager
from graph.Graph import Graph
from components.ComponentType import ComponentType

import os

from flask import Flask, request, render_template, jsonify

UPLOADS_PATH = join(dirname(realpath(__file__)))
app = Flask(__name__, template_folder='resources', static_folder='resources/static/')


# CircuitManager = CircuitManager()

# Returns the UI of the page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# app.add_url_rule('/api/<component>', 'show_user', show_user)

# Calls the detection program.
@app.route('/api/solve', methods=['POST'])
def detect():
    uploaded_file = request.files['file']

    circuit_manager = CircuitManager()
    circuit_manager.CreateCircuitFromNetListFile(uploaded_file)
    json_result = circuit_manager.Solve()

    return json_result

if __name__ == '__main__':
    app.run()
