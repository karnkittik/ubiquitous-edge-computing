import threading
from threading import Lock
import cv2
import socket
import json
import time
import argparse

class Camera:
    last_frame = None
    last_ready = None
    lock = Lock()
    running = True  # Flag to control the thread

    def __init__(self, rtsp_link):
        self.capture = cv2.VideoCapture(rtsp_link)
        if not self.capture.isOpened():
            raise ValueError(f"Failed to open RTSP stream: {rtsp_link}")
        
        thread = threading.Thread(target=self.rtsp_cam_buffer, args=(self.capture,), name="rtsp_read_thread")
        thread.daemon = True
        thread.start()

    def rtsp_cam_buffer(self, capture):
        while self.running:
            with self.lock:
                self.last_ready, self.last_frame = capture.read()
                if not self.last_ready:
                    print("Failed to read frame from stream.")
                    time.sleep(0.1)  # Sleep to prevent tight loop in case of read failure

    def getFrame(self):
        with self.lock:  # Lock while accessing shared resources
            if (self.last_ready is not None) and (self.last_frame is not None):
                return self.last_frame.copy()
            else:
                return None
    
    def stop(self):
        self.running = False
        self.capture.release()  # Release the capture when done

class BoundingBoxReceiver:
    def __init__(self, host='0.0.0.0', port=12345, hold_frames=3):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.lock = Lock()
        self.bounding_boxes = []  # To store received bounding boxes
        self.frame_counter = hold_frames  # Counter to hold boxes for a specific number of frames
        self.hold_frames = hold_frames  # Number of frames to hold boxes
        self.running = True

    def start_receiving(self):
        print("Bounding box receiver started.")
        while self.running:
            data, _ = self.server_socket.recvfrom(4096)  # Buffer size is 4096 bytes
            try:
                # Assuming the data is in JSON format
                bbox = json.loads(data.decode('utf-8'))
                with self.lock:
                    # Reset the frame counter when new bounding boxes are received
                    self.frame_counter = self.hold_frames
                    self.bounding_boxes = [bbox['detections']]  # Store the current detections
            except json.JSONDecodeError:
                print("Failed to decode JSON data.")

    def get_bounding_boxes(self):
        with self.lock:
            if self.frame_counter > 0:
                # Decrease frame counter and return the last bounding boxes
                self.frame_counter -= 1
                return self.bounding_boxes
            else:
                # Return empty if the hold time has passed
                return []

    def stop(self):
        self.running = False
        self.server_socket.close()

parser = argparse.ArgumentParser(description="RTSP Object Detection with YOLOv8")
parser.add_argument('rtsp_url', type=str, help="RTSP URL of the camera stream")
args = parser.parse_args()
# Usage
rtsp_url = args.rtsp_url
capture = Camera(rtsp_url)
bbox_receiver = BoundingBoxReceiver()

# Start the bounding box receiver in a separate thread
bbox_thread = threading.Thread(target=bbox_receiver.start_receiving, name="bbox_receiver_thread")
bbox_thread.daemon = True
bbox_thread.start()

try:
    while True:
        frame = capture.getFrame()
        if frame is not None:
            # Get the bounding boxes and draw them on the frame
            boxes = bbox_receiver.get_bounding_boxes()
            for detection in boxes:
                for box in detection:
                    # Ensure the coordinates are integers
                    x1, y1 = int(box['box']['x1']), int(box['box']['y1'])
                    x2, y2 = int(box['box']['x2']), int(box['box']['y2'])
                    conf = box['confidence']
                    cls = box['class']
                    
                    # Draw rectangle and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle
                    cv2.putText(frame, f"{cls} {conf:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the frame with bounding boxes
            cv2.imshow("RTSP Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No frame available.")

finally:
    capture.stop()
    cv2.destroyAllWindows()
