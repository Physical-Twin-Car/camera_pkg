import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        # Set up the camera
        # getal is welke USB poort 
        # werkt momenteel niet met de USB hub om alle drie de camera's tegelijk aan te hebben
        self.cameras = {
            #'right': cv2.VideoCapture(0),
            'front': cv2.VideoCapture(2),
            #'left': cv2.VideoCapture(4)
        }

        # Checken of de camera's geopend zijn
        for camera_name, cap in self.cameras.items():
            if not cap.isOpened():
                print(f"Camera {camera_name} couldn't be opened")
            else:
                print(f"Camera {camera_name} succesfully opened")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # lagere resolutie
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        cap.set(cv2.CAP_PROP_FPS, 30)


        # Publishers aanmaken voor elke camera
        self.camera_publishers = {
            #'right': self.create_publisher(Image, '/camera/right', 10),
            'front': self.create_publisher(Image, '/camera/front', 10),
            #'left': self.create_publisher(Image, '/camera/left', 10),
        }
        
        # Converteren OpenCV images naar ROS images
        self.bridge = CvBridge()

        # Publish elke 0.1s (10Hz)
        self.timer = self.create_timer(0.1, self.capture_and_publish)

    def capture_and_publish(self):
        for camera_name, cap in self.cameras.items():
            ret, frame = cap.read()

            if not ret or frame is None or frame.size == 0:
                print(f"No frame received from {camera_name}")
                continue

            # Conversie OpenCV -> ROS image
            image_msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')

            # Publish the image message for this camera
            self.camera_publishers[camera_name].publish(image_msg)
            print(f"Published frame from {camera_name} camera")



def main(args=None):
    rclpy.init(args=args) 
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
