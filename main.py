# A Web Application which takes an image from user and tells him the most colors used in
# his image.

import numpy as np
from PIL import Image # for reading image files
from flask import Flask, render_template, request


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def give_most_hex(file_path):
    my_image = Image.open(file_path).convert('RGB')
    image_array = np.array(my_image)

    # create a dictionary of unique colors with each color's count set to 0
    # increment count by 1 if it exists in the dictionary
    unique_colors = {}  # (r, g, b): count
    for column in image_array:
        for rgb in column:
            t_rgb = tuple(rgb)
            if t_rgb not in unique_colors:
                unique_colors[t_rgb] = 0
            if t_rgb in unique_colors:
                unique_colors[t_rgb] += 1

    # get a list of top ten occurrences/counts of colors from unique colors dictionary
    values = set(unique_colors.values())
    values = list(values)
    values.sort(reverse=True)

    # get only 10 highest values
    top_10 = values[0:10]

    # sorted(key_value.items(), key=lambda kv: (kv[1], kv[0]))

    # using a sorted dictionary
    sorted_values = sorted(unique_colors.values())  # Sort the values. Returns a list of values
    sorted_dict = {}

    for i in sorted_values:
        for k in unique_colors.keys():
            if unique_colors[k] == i:
                sorted_dict[k] = unique_colors[k]
                break

    # have a dictionary of top ten colors, with their counts.
    dict_of_top = {}

    for key in sorted_dict:
        if sorted_dict[key] in top_10:
            dict_of_top[key] = sorted_dict[key]

    # code to convert rgb to hex
    hex_list = []
    for key in dict_of_top:
        hex = rgb_to_hex(key)
        hex_list.append(hex)

    return hex_list


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        hexes = give_most_hex(f.stream)
        return render_template('index.html', colors_list=hexes)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
