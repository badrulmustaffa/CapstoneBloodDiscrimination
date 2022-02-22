# Done by Muhammad Mustaffa

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, SelectField, SelectMultipleField, StringField

from my_app import photos


class ProfileForm(FlaskForm):
    """ Class for the profile form """
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])


class HealthForm(FlaskForm):
    sex = SelectField('Sex', choices=['Male', 'Female', 'Non-binary'])
    condition = SelectMultipleField('Do you have any of these health conditions?',
                                    choices=['High Blood Pressure', 'History of Heart Attack',
                                             'Coronary Artery Disease',
                                             'Undiagnosed Chest Pain', 'Shortness of Breath', 'Irregular Heartbear',
                                             'Artificial Heart Valve', 'Peripheral Vascular Disease',
                                             'Congestive Heart Failure',
                                             'Diabetes', 'Kidney Disease', 'Cancer', 'Epilepsy/Seizure',
                                             'Mental Illness',
                                             'Emphysema', 'Asthma', 'Chronic Cough', 'Heart Murmur', 'Wheezing',
                                             'Stroke', 'High Cholestrol',
                                             'Thyroid Disease', 'Seasonal Allergies', 'Bleeding/Clotting Disorder',
                                             'Varicose Veins',
                                             'Gastrointestinal Disease', 'Liver Disease/Hepatitis', 'HIV',
                                             'History of Covid'])
    othercondition = StringField('Other health conditions')
