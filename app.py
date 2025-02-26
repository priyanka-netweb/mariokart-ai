from flask import Flask, send_file, Response
import cv2
import mediapipe as mp

app = Flask(__name__, static_url_path="", static_folder=".")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# OpenCV Video Capture
def is_palm_open(hand_landmarks):
    """
    Determines if the palm is open by checking if fingertips are significantly above their corresponding knuckles.
    """
    TIP_IDS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
    PIP_IDS = [3, 6, 10, 14, 18]  # Corresponding knuckles (proximal interphalangeal joints)

    open_fingers = sum(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y for tip, pip in zip(TIP_IDS, PIP_IDS))
    
    return open_fingers >= 4  # Consider the palm open if at least 4 fingers are extended


def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Flip the frame horizontally to correct mirroring
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        left_hand_open = False
        right_hand_open = False
        left_hand_closed = False
        right_hand_closed = False
        detected_hands = 0

        if result.multi_hand_landmarks:
            detected_hands = len(result.multi_hand_landmarks)  # Count hands detected

            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Check handedness
                hand_label = result.multi_handedness[idx].classification[0].label  # "Left" or "Right"
                palm_open = is_palm_open(hand_landmarks)

                if hand_label == "Left":
                    if palm_open:
                        left_hand_open = True
                    else:
                        left_hand_closed = True
                elif hand_label == "Right":
                    if palm_open:
                        right_hand_open = True
                    else:
                        right_hand_closed = True

        # Determine actions
        actions = []

        if left_hand_open and right_hand_open:
            actions.append("JUMP")
        elif left_hand_closed and right_hand_closed:
            actions.append("CROUCH")
        elif right_hand_open and left_hand_closed:
            actions.append("JUMP")
            actions.append("RIGHT")
        elif left_hand_open and right_hand_closed:
            actions.append("JUMP")
            actions.append("LEFT")
        elif right_hand_open:
            actions.append("RIGHT")
        elif left_hand_open:
            actions.append("LEFT")
        elif detected_hands == 0:
            actions.append("STILL")

        # Display actions on the frame
        action_text = " ".join(actions)
        cv2.putText(frame, action_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3, cv2.LINE_AA)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route("/")
def serve_index():
    return send_file("index.html")  # Serve index.html from the current directory

@app.route("/video")
def video():
    return send_file("video.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)