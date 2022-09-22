from keras.models import load_model
from keras_preprocessing.image import img_to_array
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import cv2
import numpy as np


model = load_model('GR.h5')

# Create gender classes
classes = {
    0: 'female',
    1: 'male'
}

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
RTC_CONFIGURATION = RTCConfiguration(
{"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
    

def callback(frame):
    img = frame.to_ndarray(format = 'bgr24')
    
    faces = face_cascade.detectMultiScale(
        image = img, scaleFactor = 1.1, minNeighbors = 3
    )

    for x, y, w, h in faces:
        # Draw rectangle over face
        cv2.rectangle(img = img, pt1 = (x, y), pt2 = (x + w, y + h), color = (0, 255, 0), thickness = 2)
        
     # Do preprocessing based on model
        face_crop = img[y:y + h, x:x + w]
        face_crop = cv2.resize(face_crop, (224, 224))
        face_crop = img_to_array(face_crop)
        face_crop = face_crop / 255
        face_crop = np.expand_dims(face_crop, axis = 0)
        
        # Predict gender
        prediction = model.predict(face_crop)[0]
        
        # Get the max accuracy
        idx = prediction.argmax(axis=-1)
        
        # Get the label using the max accuracy
        label_class = classes[idx]
        
        # Create the format for label and confidence (%) to be displayed
        label = '{}: {:2f}%'.format(label_class, prediction[idx] * 100)
        
        # # Write label and confidence above the face rectangle
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return av.VideoFrame.from_ndarray(img, format = 'bgr24')
    
    
def main():
    st.title('Real-time Gender Recognition Application')
    pages = ['Home', 'Webcam Gender Recognition', 'Audio Gender Recognition', 'About']
    
    choice = st.sidebar.selectbox('Select Page', pages)
    
    if choice == 'Home':
        html_temp_home1 = """"<div style="background-color:#6D7B8D; padding:10px">
                                            <h4 style="color:white; text-align:center;">
                                            Real-time Gender Recognition Application using OpenCV, Tensorflow and Streamlit.</h4>
                                            </div>
                                            </br>"""
                                            
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        st.write("""
                 The application has two functionalities:

                 1. Real time gender recognition using webcam feed.

                 2. Real time gender recognization using voice.

                 """)
        
    elif choice == "Webcam Gender Recognition":
        st.header("Webcam Live Feed")
        st.write("Click on start to use webcam and detect your Gender")
        webrtc_streamer(key = 'example',
                        rtc_configuration = RTC_CONFIGURATION,
                        video_frame_callback= callback,
                        media_stream_constraints = {
                            'video': True,
                            'audio': False
                            }
                        )
        
    elif choice == "About":
        st.subheader("About this app")
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    Real time face emotion detection application using OpenCV, Tensorflow, and Streamlit.</h4>
                                    </div>
                                    </br>"""
                                    
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#98AFC7;padding:10px">
                             		<h4 style="color:white;text-align:center;">This Application was developed by: Penda Silas, Ogunjimi Ayobami, Ebenezer Acquah, Olabisi Oluwale Anthony, 
                                    Raphael Okai, and Oluwatimilehin Folarin.</h4>
                                    <h4 style="color:white;text-align:center;">Need a guide on how to go about such a project? [Github] (https://github.com/SilasPenda/Real-time-Gender-Detection).</h4>
                             		<h4 style="color:white;text-align:center;">Thanks for Visiting</h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass
    
    
if __name__ == "__main__":
    main()