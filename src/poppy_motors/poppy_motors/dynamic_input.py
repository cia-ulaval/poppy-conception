from motors import MotorCommands
import time
import pandas as pd
wait_time = 0.7
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

    def export_positions(position):
        positions = commad.get_all_present_position_MX()
        print(positions)
        positions = pd.DataFrame((positions.items()), columns=["motor_id", "value"])
        positions.to_csv(f"positions_{position}.csv", index=False)
        return None
    
    mode = int(input("Modes : \n1=try positions\n2=floss\n3=dab\n"))
    
    while True:
        if mode == 1:
            
            try:
                id = int(input("ID du moteur à set position : "))
                if id == 100:
                    compteur = input("Numéro du fichier que tu veux : ")
                    export_positions(compteur)
                else:
                    pourcentage = float(input("Position (%) : "))
                    if id in commad.get_motor_ids() and pourcentage in range(1, 100, 1):
                        commad.set_goal_percent(id, pourcentage)
                    else:
                        print("id non valide\nOU pourcentage pas entre 1 et 99")
                        continue
            except ValueError as e:
                print("invalid input")
                continue
        
        if mode == 2:
            def position_1():
                pos_1 = pd.read_csv("positions_11.csv")
                pos_1 = pos_1.set_index("motor_id")["value"].to_dict()
                commad.set_all_goal(pos_1)
                time.sleep(wait_time)

            def position_2():
                pos_2 = pd.read_csv("positions_12.csv")
                pos_2 = pos_2.set_index("motor_id")["value"].to_dict()
                commad.set_all_goal(pos_2)
                time.sleep(wait_time)
            
            def position_3():
                pos_3 = pd.read_csv("positions_13.csv")
                pos_3 = pos_3.set_index("motor_id")["value"].to_dict()
                commad.set_all_goal(pos_3)
                time.sleep(wait_time)

            def position_4():
                position_2()

            def position_5():
                position_1()
            
            def position_6():
                pos_6 = pd.read_csv("positions_14.csv")
                pos_6 = pos_6.set_index("motor_id")["value"].to_dict()
                commad.set_all_goal(pos_6)
                time.sleep(wait_time)

    

            while True:
                position_1()
                position_2()
                position_3()
                position_4()
                position_5()
                position_6()
        
        if mode == 3:
            pos_dab = pd.read_csv("positions_70.csv")
            pos_dab = pos_dab.set_index("motor_id")["value"].to_dict()
            commad.set_all_goal(pos_dab)

dynamic_set()







        
