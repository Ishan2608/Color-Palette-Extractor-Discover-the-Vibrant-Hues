# A Web Application which takes an image from user and tells him the most colors used in
# his image.

import numpy as np
# import matplotlib
from PIL import Image # for reading image files
from flask import Flask, render_template, request


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def give_most_hex(file_path):
    my_image = Image.open(file_path).convert('RGB')
    image_array = np.array(my_image)
    # matplotlib.pyplot.imshow(my_image)

    # create a dictionary of unique colors with each color's count set to 0
    unique_colors = {}  # (r, g, b): count
    for column in image_array:
        for rgb in column:
            t_rgb = tuple(rgb)
            if t_rgb not in unique_colors:
                unique_colors[t_rgb] = 0
                # break

    # print(unique_colors)

    # add counts to colors of unique colors dictionary
    for clrs in unique_colors:
        for column in image_array:
            for rgb in column:
                t_c = tuple(rgb)
                if t_c == clrs:
                    unique_colors[clrs] += 1

    # print(unique_colors)

    # get a lost of top ten occurrences/counts of colors from unique colors dictionary
    values = set(unique_colors.values())
    values = list(values)
    values.sort()
    values.reverse()

    top_10 = []
    for i in range(10):
        top_10.append(values[i])

    # have a dictionary of top ten colors, with their counts.
    dict_of_top = {}

    for key in unique_colors:
        if unique_colors[key] in top_10:
            dict_of_top[key] = unique_colors[key]

    # print(dict_of_top)

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
        # f.save(f.filename)
        hexes = give_most_hex(f.stream)
        return render_template('index.html', colors_list=hexes)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
