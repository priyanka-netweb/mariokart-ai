from flask import Flask, send_file, Response, jsonify
import cv2
import mediapipe as mp
import time

app = Flask(__name__, static_url_path="", static_folder=".")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Control keys (acts like keyboard state)
controlKeys = {
    "JUMP": False,
    "CROUCH": False,
    "LEFT": False,
    "RIGHT": False,
    "FIRE": False,
}

def is_palm_open(hand_landmarks):
    """Detect if palm is open based on fingertip positions."""
    TIP_IDS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
    PIP_IDS = [3, 6, 10, 14, 18]  # Corresponding knuckles

    open_fingers = sum(
        hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y
        for tip, pip in zip(TIP_IDS, PIP_IDS)
    )
    return open_fingers >= 4  # If 4+ fingers are extended, palm is open

def generate_frames():
    """Continuously detect hand gestures and send them to the frontend."""
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Mirror the image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Reset all control keys before detecting new state
        controlKeys.update({"JUMP": False, "CROUCH": False, "LEFT": False, "RIGHT": False, "FIRE": False})

        left_hand_open, right_hand_open = False, False
        left_hand_closed, right_hand_closed = False, False
        detected_hands = 0

        if result.multi_hand_landmarks:
            detected_hands = len(result.multi_hand_landmarks)

            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

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

        # Determine actions (multiple actions possible)
        if left_hand_open and right_hand_open:
            controlKeys["JUMP"] = True
        if left_hand_closed and right_hand_closed:
            controlKeys["CROUCH"] = True
        if right_hand_open and detected_hands == 1:
            controlKeys["RIGHT"] = True
            controlKeys["JUMP"] = True
        if left_hand_open and detected_hands == 1:
            controlKeys["LEFT"] = True
            controlKeys["JUMP"] = True
        if left_hand_closed and detected_hands == 1:
            controlKeys["LEFT"] = True
        if right_hand_closed and detected_hands == 1:
            controlKeys["RIGHT"] = True
        if left_hand_open and detected_hands == 2 or right_hand_open and detected_hands == 2:
            controlKeys["FIRE"] = True

 # Display actions on the frame
        action_text = " ".join({k: v for k, v in controlKeys.items() if v})
        cv2.putText(frame, action_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3, cv2.LINE_AA)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(0.001)  # Prevent excessive CPU usage

# Start hand tracking in a separate thread

@app.route("/")
def serve_index():
    return send_file("index.html")

@app.route("/video")
def video():
    return send_file("video.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/controls")
def get_controls():
    """Returns the current state of control keys."""
    return jsonify(controlKeys)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)