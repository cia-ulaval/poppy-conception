from motors import MotorCommands
import time
# Hola que tal

def dynamic_set():

    def _set_initial_postion(motor_commands):
        
        motor_commands.set_goal(21, 2048)
        motor_commands.set_goal(22, 2048)
        motor_commands.set_goal(23, 2048)
        motor_commands.set_goal(24, 2048)
        motor_commands.set_goal(25, 2048)
        motor_commands.set_goal(11, 2048)
        motor_commands.set_goal(12, 2048)
        motor_commands.set_goal(13, 2048)
        motor_commands.set_goal(14, 2048)
        motor_commands.set_goal(15, 2048)
        motor_commands.set_goal(31, 2048)
        motor_commands.set_goal(32, 2048)
        motor_commands.set_goal(33, 2048)
        motor_commands.set_goal(34, 2048)
        motor_commands.set_goal(35, 2048)
        motor_commands.set_goal(36, 512)
        motor_commands.set_goal(37, 512)
        motor_commands.set_goal(41, 2048)
        motor_commands.set_goal(42, 2048)
        motor_commands.set_goal(43, 2048)
        motor_commands.set_goal(44, 2048)
        motor_commands.set_goal(51, 2048)
        motor_commands.set_goal(52, 2048)
        motor_commands.set_goal(53, 2048)
        motor_commands.set_goal(54, 2048) 
    
    

    commad = MotorCommands()
    commad.reboot_all_motors()
    _set_initial_postion(commad)
    print(commad.get_motor_ids())
    commad.torque_enable_all()
    commad.set_goal_percent(31, 90)
    commad.set_goal_percent(34, 80)

    def export_positions():
        positions = commad.get_all_present_position_MX()
        return positions
    while True:
        try:
            id = int(input("ID du moteur à set position : "))
            pourcentage = float(input("Position (%) : "))
            commad.set_goal_percent(id,pourcentage)
        except ValueError as e:
            print("invalid input")
            continue
dynamic_set()

def floss():
    def _set_initial_postion(motor_commands):
        
        motor_commands.set_goal(21, 2048)
        motor_commands.set_goal(22, 2048)
        motor_commands.set_goal(23, 2048)
        motor_commands.set_goal(24, 2048)
        motor_commands.set_goal(25, 2048)
        motor_commands.set_goal(11, 2048)
        motor_commands.set_goal(12, 2048)
        motor_commands.set_goal(13, 2048)
        motor_commands.set_goal(14, 2048)
        motor_commands.set_goal(15, 2048)
        motor_commands.set_goal(31, 2048)
        motor_commands.set_goal(32, 2048)
        motor_commands.set_goal(33, 2048)
        motor_commands.set_goal(34, 2048)
        motor_commands.set_goal(35, 2048)
        motor_commands.set_goal(36, 512)
        motor_commands.set_goal(37, 512)
        motor_commands.set_goal(41, 2048)
        motor_commands.set_goal(42, 2048)
        motor_commands.set_goal(43, 2048)
        motor_commands.set_goal(44, 2048)
        motor_commands.set_goal(51, 2048)
        motor_commands.set_goal(52, 2048)
        motor_commands.set_goal(53, 2048)
        motor_commands.set_goal(54, 2048) 
    
    

    commad = MotorCommands()
    commad.reboot_all_motors()
    _set_initial_postion(commad)
    print(commad.get_motor_ids())
    commad.torque_enable_all()
    commad.set_goal_percent(31, 90)
    commad.set_goal_percent(34, 80)
 
    def position_1():
        commad.set_goal_percent(51,35)
        commad.set_goal_percent(52, 35)
        commad.set_goal_percent(53, 10)
        commad.set_goal_percent(41, 1)
        commad.set_goal_percent(42, 1)
        commad.set_goal_percent(43, 10)
        time.sleep(3)

    def position_2():
        commad.set_goal_percent(52, 1)
        commad.set_goal_percent(42, 35)
        time.sleep(3)
    
    def position_3():
        commad.set_goal_percent(52, 25)
        commad.set_goal_percent(41, 22)
        commad.set_goal_percent(42, 1)
        time.sleep(3)

    def position_4():
        commad.set_goal_percent(42, 25)
        commad.set_goal_percent(41, 1)
        commad.set_goal_percent(52, 1)
        time.sleep(3)

    def position_5():
        commad.set_goal_percent(51, 25)
        commad.set_goal_percent(52, 15)
        commad.set_goal_percent(42, 1)
        time.sleep(3)
    
    def position_6():
        commad.set_goal_percent(51, 20)
        commad.set_goal_percent(52, 10)
        time.sleep(3)

    def position_7():
        position_1()
        
    
    while True:
        # position_1()
        # position_2()
        # position_3()
        position_4()
        # position_5()
        # position_6()
        # position_7()

# floss()




        
