from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from my_app.algorithm.forms import TesterForm
from my_app.models import Tester
from datetime import datetime
from skimage import io
from my_app import db, images
from keras.models import model_from_json
from my_app.config import Config
from pathlib import Path

import tensorflow
import numpy as np
import os
from PIL import Image


algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')

# opening and store file in a variable
model_json_path = Path(__file__).parent.parent.joinpath("algorithm").joinpath("model.json")
json_file = open(model_json_path, 'r')
loaded_model_json = json_file.read()
json_file.close()

# use Keras model_from_json to make a loaded model
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
model_h5_path = Path(__file__).parent.parent.joinpath("algorithm").joinpath("model.h5")
loaded_model.load_weights(model_h5_path)
print("Loaded Model from disk")

# compile and evaluate loaded model
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


@algorithm_bp.route('/tester', methods=['GET', 'POST'])
@login_required
def submit():
    form = TesterForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = 'default.png'

        if 'blood_image' in request.files:

            if request.files['blood_image'].filename != '':
                filename = images.save(request.files['blood_image'])

                infile = Config.UPLOADED_IMAGES_DEST.joinpath(filename)
                filename.replace('tif', 'png')
                outfile = Config.UPLOADED_IMAGES_DEST.joinpath(filename)
                im = Image.open(infile)
                out = im.convert('RGB')
                out.save(outfile, 'PNG')

        output = predict(request.files['blood_image'])
        # result to be changed when algorithm is ready
        registration = Tester.query.filter_by(kit_id=form.kit_code.data).one()
        registration.blood_image = filename
        registration.result = output
        registration.date_posted = datetime.now()
        db.session.commit()

        flash('Your entry has been submitted')

        return redirect(url_for('algorithm_bp.confirm', kit_ID=form.kit_code.data))
    return render_template('algorithm_submit.html', entry=form)


@algorithm_bp.route('/confirmation/<kit_ID>', methods=['GET', 'POST'])
@login_required
def confirm(kit_ID):
    result = Tester.query.filter_by(kit_id=kit_ID).one()
    return render_template('algorithm_confirm.html', result=result)


@algorithm_bp.route('/blood_image/<filename>')
def blood_image(filename):
    return send_from_directory(Config.UPLOADED_IMAGES_DEST, '/database', filename=filename, as_attachment=True)


def predict(sample):
    imgData = sample#request.files['blood_image']
    x = io.imread(imgData)
    x = tensorflow.image.resize(x / 255, (200, 200))

    # with graph.as_default():
    out = loaded_model.predict(np.expand_dims(x, axis=0))
    print(out)
    if int(round(out[0][0])) == 1:
        output = 'baseline'
    else:
        output = '6 minutes'

    return output
