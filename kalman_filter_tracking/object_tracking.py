
# Import python libraries
import cv2
import copy
from detectors import Detectors
from tracker import Tracker
import numpy as np


def main():

    # Create opencv video capture object
    cap = cv2.VideoCapture('G:/cmu/colonoscopy/New folder/Cold.mp4')
    #cap = cv2.VideoCapture('G:/cmu/colonoscopy/imagemark/Color-Tracker-master/Retroflect-at-end.mp4')

    # Create Object Detector
    detector = Detectors()

    # Create Object Tracker
    tracker = Tracker(160, 1000, 5, 100)

    # Variables initialization
    skip_frame_count = 0
    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]
    pause = False
    num = 0
    frame_num = 0

    # Infinite loop to process video frames
    while(True):
        frame_num += 1
        print(frame_num)
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = frame[30:550,400:930]
        #frame = frame[40:400,130:450]

        # Make copy of original frame
        orig_frame = copy.copy(frame)

        # Skip initial frames that display logo
        if (skip_frame_count < 15):
            skip_frame_count += 1
            continue

        # Detect and return centeroids of the objects in the frame
        centers = detector.Detect1(orig_frame)

        # If centroids are detected then track them
        if (len(centers) > 0):
            text = 'Biopsy'
            cv2.putText(orig_frame,text,(100,100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255),2, lineType=cv2.LINE_AA)
            # Track object using Kalman Filter
            tracker.Update(centers)

            # For identified object tracks draw tracking line
            # Use various colors to indicate different track_id
            for i in range(len(tracker.tracks)):
                if (len(tracker.tracks[i].trace) > 1):
                    for j in range(len(tracker.tracks[i].trace)-1):
                        # Draw trace line
                        x1 = tracker.tracks[i].trace[j][0][0]
                        y1 = tracker.tracks[i].trace[j][1][0]
                        x2 = tracker.tracks[i].trace[j+1][0][0]
                        y2 = tracker.tracks[i].trace[j+1][1][0]
                        clr = tracker.tracks[i].track_id % 9
                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                 track_colors[clr], 2)
            # Display the resulting tracking frame
            cv2.imshow('Tracking', frame)

        # Display the original frame
        cv2.imshow('Original', orig_frame)
        print(num)

        # Slower the FPS
        cv2.waitKey(20)

        # Check for key strokes
        k = cv2.waitKey(50) & 0xff
        if k == 27:  # 'esc' key has been pressed, exit program.
            break
        if k == 112:  # 'p' has been pressed. this will pause/resume the code.
            pause = not pause
            if (pause is True):
                print("Code is paused. Press 'p' to resume..")
                while (pause is True):
                    # stay in this loop until
                    key = cv2.waitKey(30) & 0xff
                    if key == 112:
                        pause = False
                        print("Resume code..!!")
                        break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # execute main
    main()
