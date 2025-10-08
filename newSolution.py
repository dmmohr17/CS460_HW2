import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Walk(Node):
	def __init__(self):
		super().__init__('Walk')
		self.cmd_pub = self.create_publisher(Twist,'/cmd_vel', 10)
		timer_period = 0.2 # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.time = 0
		self.whisker = 5.0
		self.left = 0.0
		self.right = 10.0
		self.direction = -1
		self.linear_speed = 0.8
		self.move_cmd = Twist()
		self.move_cmd.linear.x = self.linear_speed
		self.subscription = self.create_subscription(
			LaserScan,
			'/base_scan',
			self.sensor_callback,
			10)
		#self.subscription # prevent unused variable warning

	def sensor_callback(self, msg):
		middle_sensor = int(len(msg.ranges) / 2)
		quarterAngle = int(middle_sensor / 2)
		front = msg.ranges[middle_sensor]
		frontLeft = msg.ranges[middle_sensor - quarterAngle]
		frontRight = msg.ranges[middle_sensor + quarterAngle]
		print("Sensor: " + str(front))
		self.whisker = front
		self.left = frontLeft
		self.right = frontRight

	def forward(self):
		self.move_cmd.linear.x = self.linear_speed

	def timer_callback(self):
		if(self.whisker < 2.0):
			if(self.left < self.right and self.direction == -1):
				self.direction = 0
				self.move_cmd.angular.z = -2.0
			elif(self.direction == -1): # self.left > self.right
				self.direction = 1
				self.move_cmd.angular.z = 2.0
			else:
				if(self.direction == 0):
					self.move_cmd.angular.z = -2.0
				else:
					self.move_cmd.angular.z = 2.0
			self.move_cmd.linear.x = 0.0
		elif(self.left < 0.5 and (self.direction == -1 or self.direction == 0)):
			self.direction = 1
			self.move_cmd.angular.z = 1.0
			self.move_cmd.linear.x = 0.0
		elif(self.right < 0.5 and (self.direction == -1 or self.direction == 1)):
			self.direction = 0
			self.move_cmd.angular.z = -1.0
			self.move_cmd.linear.x = 0.0
		else:
			if(self.direction != -1):
				self.direction = -1
			self.move_cmd.angular.z = 0.0
			self.move_cmd.linear.x = self.linear_speed
		self.cmd_pub.publish(self.move_cmd)
		#self.move_cmd.linear.x = self.linear_speed

def main(args = None):
	rclpy.init(args=args)
	turtle_controller = Walk()
	rclpy.spin(turtle_controller)
	turtle_controller.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
    main()
