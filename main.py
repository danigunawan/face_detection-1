from yoloface import yoloface
from mtcnn import mtcnn
from haarcascade import haarcascade
from retina_face import retina_face
from dsfd import dsfd
from S3FD import s3fd
from centerface import centerface
from face_boxes import FaceBoxes

from yoloface.utils import *
import cv2
import time

__all_detectors = [
    yoloface,
    mtcnn,
    haarcascade,
    retina_face,
    dsfd,
    s3fd,
    centerface,
    FaceBoxes
]


def do_detect(stream_path, detector, save=False, blur_faces=False):
    wind_name = 'Face Detection using ' + detector.Name
    cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(stream_path)
    count = 0

    while True:

        has_frame, frame = cap.read()
        count += 1

        # Stop the program if reached end of video
        if not has_frame:
            print('[i] ==> Done processing!!!')
            cv2.waitKey(1000)
            break

        # Uncomment this if you want to skip the frames
        # This skips to every 70th frame
        # if count % 70 != 0:
        #     continue

        start_time = time.time()
        faces = detector.detect_faces(frame)
        print("--- %s seconds ---" % (time.time() - start_time))

        print('[i] ==> # detected faces: {}'.format(len(faces)))
        print('#' * 60)

        # initialize the set of information we'll displaying on the frame
        info = [
            ('{}: Number of faces detected'.format(detector.Name), '{}'.format(len(faces)))
        ]

        for (i, (txt, val)) in enumerate(info):
            text = '{}: {}'.format(txt, val)
            cv2.putText(frame, text, (10, (i+1) * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_RED, 2)

        for f in faces:
            b = f.bbox
            draw_predict(frame, f.conf, b[0], b[1], b[2], b[3], blur_faces, f.name)

        if save:
            cv2.imwrite('imgs/new/' + detector.Name + '' + str(count) + '.png', frame)
            return

        cv2.imshow(wind_name, frame)

        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            print('[i] ==> Interrupted by user!')
            break

    cap.release()
    cv2.destroyAllWindows()

    print('==> All done!')
    print('***********************************************************')


if __name__ == '__main__':
    # retina_face.Recognition = True
    # do_detect('sut_KS_48.mp4', retina_face, save=True, blur_faces=True)
    do_detect('sut_KS_48.mp4', retina_face)
    # for detector in __all_detectors:
    #    do_detect('sut_KS_48.mp4', detector, True, True)
