import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os

st.set_option('deprecation.showfileUploaderEncoding', False)

def cartoon_filter(image):
    image=np.array(image.convert('RGB'))
    numDownSamples = 2 
    numBilateralFilters = 5  

    img_color = image
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)

    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)


    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)

    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    img_edge = cv2.adaptiveThreshold(img_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)

    return cv2.bitwise_and(img_color, img_edge)


def about():
    st.write(
        '''
        **Cartoonizer** 

        How does it work ?? 

        1.Apply a bilateral filter to reduce the color palette of the image.

        2.Convert the original color image into grayscale.

        3.Apply a median blur to reduce image noise.

        4.Use adaptive thresholding to detect and emphasize the edges in an edge mask.

        5.Combine the color image from step 1 with the edge mask from step 4.

        '''
    )


def main():
    st.title("Cartoonizer App :sunglasses:")
    st.write("**Using OpenCV**")

    activities=["Home","About"]
    choice = st.sidebar.selectbox("Select",activities)

    if choice == "Home":
        st.write("Check out About section to know more")

        image_file=st.file_uploader("Upload image",type=['jpeg','png','jpg','webp'])

        if image_file is not None:

            image=Image.open(image_file)

            if st.button("Cartoonize"):

                result_img= cartoon_filter(image=image)
                st.image(result_img,use_column_width=True)
                st.success("Your image has been Cartoonized")

    elif choice == "About":
        about()


if __name__ == "__main__" :
    main()



   