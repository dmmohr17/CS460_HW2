import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import math
from nav_msgs.msg import Odometry

class Walk(Node):
    def __init__(self):
        super().__init__('Walk')
        self.cmd_pub = self.create_publisher(Twist,'/cmd_vel', 10)
        timer_period = 0.01 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.time = 0
        self.x = 0
        self.y = 0
        self.whisker = 5.0
        self.whisker_array =[]
        self.degrees = 0
        dimension = 16 * 4  #split each coordinate into 4 boxes, let robot start in the center of the array
        self.arr = [[0] * dimension for _ in range(dimension)]
        '''self.arr = [[[0,0]] * dimension for _ in range(dimension)]
        for i in range(0, dimension):
            for j in range(0, dimension):
                if i >= dimension/2 and j >= dimension/2:
                    self.arr[i][j][1] = i+j-64-64
                elif i >= dimension/2 and j <= dimension/2:
                    self.arr[i][j][1] = i-64+64-j
                elif i <= dimension/2 and j >= dimension/2:
                    self.arr[i][j][1] = 64-i+j-64
                elif i <= dimension/2 and j <= dimension/2:
                    self.arr[i][j][1] = 64-i+64-j
        '''
        #print(self.arr)
        self.linear_speed = 0.0
        self.move_cmd = Twist()
        self.move_cmd.linear.x = self.linear_speed
        robocallback_temp = (lambda : self.move_robot(0,0))
        self.timer = self.create_timer(timer_period, robocallback_temp)
        self.subscription = self.create_subscription(
            LaserScan,
            '/base_scan',
            self.sensor_callback,
            10)
        #super().__init__('Track')
        self.startTime = time.time()
        self.time = 0
        self.maxDistance = 0
        self.current_distance = 0
        self.isStart = False
        self.startPos = [0, 0]
        self.subscription = self.create_subscription(
            Odometry,
            '/ground_truth',
            self.listener_callback,
            10)
        #self.subscription # prevent unused variable warning

    def displayMap(self,list2d):
    # 2d array - unknown 0, 1 wall, 2 open
    # all unknown ░
        size = len(list2d)
        class fourpix:
            def __init__(self,topleft,topright, bottomleft, bottomright):
                self.a = [0,0,0,0]

                self.a[0] = (topleft)
                self.a[1]  = (topright)
                self.a[2]  = (bottomleft)
                self.a[3]  = (bottomright)
            def getChar(self):
                if all(x == 0 for x in self.a):
                    return '0'
                if all(x == 1 for x in self.a):
                    return '█'
                if all(x == 2 for x in self.a):
                    return ' '
                if (self.a[1] == self.a[2] == self.a[3] == 1):
                    return '▟'
                if (self.a[0] == self.a[2] == self.a[3] == 1):
                    return '▙'
                if (self.a[0] == self.a[1] == self.a[3] == 1):
                    return '▜'
                if (self.a[0] == self.a[1] == self.a[2] == 1):
                    return '▛'
                if (self.a[0] == self.a[1] == 1 and sum(self.a) == 2):
                    return '▀'
                if (self.a[2] == self.a[3] == 1 and sum(self.a) == 2):
                    return '▄'
                if (self.a[1] == self.a[2] == 1 and sum(self.a) == 2):
                    return '▐'
                if (self.a[0] == self.a[3] == 1 and sum(self.a) == 2):
                    return '▌'
                if (self.a[0] == 1):
                    return '▘'
                if (self.a[1] == 1):
                    return '▝'
                if (self.a[2] == 1):
                    return '▖'
                if (self.a[3] == 1):
                    return '▗'
                return 'X'
    
        for y in range(0,size,1):
            append = ''
            for x in range(0,size,1):
                append = append+str(list2d[y][x])
            print(append)
    def fill_array(self):
        for i in range(0,270):
            angle = self.degrees-135+i
            curr_val =int(4*self.whisker_array[i])
            j = 0
            x_distance=0
            y_distance=0
            while (j < curr_val):
                x_distance = int(j * math.cos(math.radians(angle)))
                y_distance = int(j * math.sin(math.radians(angle)))
                j+=1
                self.arr[self.x+x_distance][self.y+y_distance]=2
            if (self.whisker_array[i]!=5):
                self.arr[self.x+x_distance][self.y+y_distance]=1
        #self.displayMap(self.arr)
        for i in range(0,len(self.arr)):
            pass
            #print(self.arr[i])
    def move_robot(self,x,y):
        #print("self.x")
        #print(self.x)
        if (self.x > x + 0.1):
            if(self.degrees >` 182 or self.degrees < 178):
                print(self.degrees)
                if(self.degrees>182):
                    #print(self.degrees)
                    self.move_cmd.angular.z = -2.0
                    self.cmd_pub.publish(self.move_cmd)
                if(self.degrees<178):
                    #print(self.degrees)
                    self.move_cmd.angular.z = 2.0
                    self.cmd_pub.publish(self.move_cmd)
        else:
            self.move_cmd.angular.z = 0.0
            self.cmd_pub.publish(self.move_cmd)
        if(True):
            pass
            #self.move_cmd.angular.z = 2.0
            #self.move_cmd.linear.x = 0.0 
        else:
            self.move_cmd.angular.z = 0.0
            self.move_cmd.linear.x = 2.0
        self.cmd_pub.publish(self.move_cmd)
        
    def sensor_callback(self, msg):
        middle_sensor = int(len(msg.ranges) / 2)
        self.whisker_array = msg.ranges
        #print("Message" + str(msg))
        front = msg.ranges[middle_sensor]
        #print("Sensor: " + str(front))
        #print(len(msg.ranges))
        self.whisker = front
        self.fill_array()
            
    def listener_callback(self, msg):
        w = msg.pose.pose.orientation.w
        z = msg.pose.pose.orientation.z
        theta = (2.0 * math.atan2(z,w))
        degrees = math.degrees(theta)
        if(degrees<0):
            degrees+=360
        self.degrees = degrees
        x = msg.pose.pose.position.x+8
        y = msg.pose.pose.position.y+8
        self.x = int(x*4)
        self.y = int(y*4)

        if self.isStart == False:
            self.startPos = [x, y]
            self.isStart = True

        dx = x - self.startPos[0]
        dy = y - self.startPos[1]
        distanceTraveled = math.sqrt(dx * dx + dy * dy)

        curTime = time.time()
        elapsed = curTime - self.startTime

        print("Elapsed Time: " + str(elapsed))
        print("Distance: " + str(distanceTraveled))

    def timer_callback(self):
        if(self.whisker < 2.0):
            self.move_cmd.angular.z = 2.0
        else:
            self.move_cmd.angular.z = 0.0
        self.cmd_pub.publish(self.move_cmd)
        #self.move_cmd.linear.x = self.linear_speed

def main(args = None):
    rclpy.init(args=args)
    turtle_controller = Walk()
    #tracker_node = Tracker()
    #rclpy.spin(tracker_node)
    rclpy.spin(turtle_controller)
    #tracker_node.destroy_node()
    turtle_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

