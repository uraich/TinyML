#!/usr/bin/python3

def UpdateVelocity(new_samples):
    print(data_index)
    current_velocity[0] = data_index
    current_velocity[1] = data_index
    current_velocity[2] = data_index
    return [current_velocity[0],current_velocity[1],current_velocity[2]]

data_index = 1
velocities = []
current_velocity = [0.0,0.0,0.0]

for i in range(5):
    print(velocities)
    v = UpdateVelocity(1)
    print(velocities)
    velocities.append(v)
    print(velocities)
    print()
    data_index += 1
    
