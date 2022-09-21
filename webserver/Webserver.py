import json
from os.path import join, dirname, realpath
from graph.Graph import Graph
from components.ComponentType import ComponentType
from circuit.CircuitManager import CircuitManager
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

@app.route('/draw', methods=['GET', 'POST'])
def draw():
    test = request.values['test']
    print("worked")

    return render_template('index.html')


@app.route('/api/add_resistor', methods=['POST'])
def add_resistor():
    # CircuitManager.AddComponent(COMPONENT.RESISTOR)
    print("resistor")
    return "test"


# Calls the detection program.
@app.route('/api/detect', methods=['POST'])
def detect():
    pass
    '''

    file = request.files['file']

    if request.values:
        resistor_type = int(request.values['type'])

    else:
        resistor_type = None

    location = f'{os.getcwd()}\\data\\images\\{file.filename}'

    try:

        with open(location, 'wb') as target:
            file.save(target)

        resistor, resistor_image = Detector().detect(location, resistor_type)

        resistor_image_byte_stream = resistor_image.byte_stream()

        resistor_image_byte_stream = resistor_image_byte_stream.decode('utf-8')

        resistor_colours = resistor.colours()

        if resistor_type is None:
            resistor_type = resistor.get_number_of_bands()

        return jsonify(colours=resistor_colours, type=resistor_type, image=resistor_image_byte_stream,
                       valid=resistor.valid, error='')

    except Exception as error:
        print(error)

        colours = [None, None, None, None, None, None]

        if resistor_type is None:
            resistor_type = 6

        return jsonify(colours=colours, type=resistor_type, image=None, valid=False, error=str(error))
        
    '''


@app.route('/api/validate', methods=['POST'])
def validate():
    pass
    '''
    resistor_bands_colours = request.values["resistor_bands"]

    resistor_bands_colours = json.loads(resistor_bands_colours)

    resistor = Resistor(resistor_bands_colours)

    digit_band_colours = resistor.get_digit_band_colours(resistor_bands_colours)

    valid = resistor.check_valid(digit_band_colours)

    return jsonify(valid=valid)
    
    '''


if __name__ == '__main__':
    app.run()
