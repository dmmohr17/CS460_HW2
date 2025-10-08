import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Walk(Node):
	def __init__(self):
		super().__init__('Walk')
		self.cmd_pub = self.create_publisher(Twist,'/cmd_vel', 10)
		timer_period = 0.1 # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.time = 0
		self.whisker = 5.0
		self.linear_speed = 0.8
		self.move_cmd = Twist()
		self.move_cmd.linear.x = self.linear_speed
		# self.move_cmd.angular.z = 0.0
		
		self.dt = 0.1
		self.e_prev = 0.0 # tracks previous error
		self.e_sum = 0.0 # sum of all errors
		self.e = 0.0 # current error 
		self.dedt = 0.0 # derivative
		self.target = 1.0 # target travel
		self.K_P = 1.0
		self.K_I = 1.0
		self.K_D = 0.0
		self.u = 0
		
		self.subscription = self.create_subscription(
			LaserScan,
			'/base_scan',
			self.sensor_callback,
			10)
		#self.subscription # prevent unused variable warning

	def sensor_callback(self, msg):
		middle_sensor = int(len(msg.ranges) / 2)
		front = msg.ranges[middle_sensor]
		# print("Sensor: " + str(front))
		self.whisker = front
	
	def forward(self):
		self.move_cmd.linear.x = self.linear_speed # = self.whisker / 5

	def timer_callback(self):
		self.e = self.whisker - self.target
		self.e_sum = self.e_sum + (self.e * self.dt)
		self.dedt = (self.e - self.e_prev) / self.dt

		"""
		if(self.travel == 0):
			self.dedt = 0
		else:
			self.dedt = (self.e - self.e_prev) / self.travel
		"""
		# testing this
		MAX_E_SUM = 10.0
        self.e_sum = max(-MAX_E_SUM, min(self.e_sum, MAX_E_SUM))
	
		self.u = self.K_P * self.e + self.K_I * self.e_sum + self.K_D * self.dedt

		# testing this also
        max_speed = 1.0  # m/s
        self.move_cmd.linear.x = max(0.0, min(self.u, max_speed))

		self.e_prev = self.e
		# self.move_cmd.linear.x = self.travel
		if(self.whisker < 2.0):
			self.move_cmd.angular.z = 2.0
		else:
			self.move_cmd.angular.z = 0.0
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
