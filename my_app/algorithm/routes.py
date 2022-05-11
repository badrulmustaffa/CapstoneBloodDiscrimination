from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from my_app.algorithm.forms import TesterForm
from my_app.models import Tester
from datetime import datetime
from skimage import io
from my_app import db, images
from keras.models import model_from_json

import tensorflow
import numpy as np
import os

algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')


# opening and store file in a variable

#json_file = open(url_for('algorithm', filename='model.json'),'r')
#json_file = open('model.json','r')
model_json_path = "C:\\Users\\farha\\PycharmProjects\\CapstoneBloodDiscrimination\\my_app\\algorithm\\model.json"
json_file = open(model_json_path, 'r')

loaded_model_json = json_file.read()
json_file.close()

# use Keras model_from_json to make a loaded model

loaded_model = model_from_json(loaded_model_json)

# load weights into new model
model_h5_path = "C:\\Users\\farha\\PycharmProjects\\CapstoneBloodDiscrimination\\my_app\\algorithm\\model.h5"
loaded_model.load_weights(model_h5_path)
print("Loaded Model from disk")

# compile and evaluate loaded model

loaded_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])




@algorithm_bp.route('/tester', methods=['GET', 'POST'])
@login_required
def submit():
    form = TesterForm()
    if request.method == 'POST' and form.validate_on_submit():

        filename = 'default.png'

        if 'blood_image' in request.files:

            if request.files['blood_image'].filename != '':

                filename = images.save(request.files['blood_image'])

        output = predict()
        # result to be changed when algorithm is ready
        registration = Tester(kit_id=form.kit_code.data, blood_image=filename,
                              result=output, date_posted=datetime.now())
        db.session.add(registration)
        db.session.commit()
        flash('Your entry has been submitted')

        return redirect(url_for('algorithm_bp.submit'))
    return render_template('algorithm_submit.html', entry=form)


def predict():
    imgData = request.files['blood_image']
    x = io.imread(imgData)
    x = tensorflow.image.resize(x/255,(200,200))

    # with graph.as_default():
    out= loaded_model.predict(np.expand_dims(x, axis = 0))
    print(out)
    if int(round(out[0][0])) == 1:
        output = 'baseline'
    else:
        output = '6 minutes'

    return output
