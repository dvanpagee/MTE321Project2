import math
import matplotlib.pyplot as plt

## Parameters

# Inputs
power_hp = 170
power_torque = power_hp * 550 * 12

# Misc
first_letter = 12 
last_letter = 4
speed_rpm = 700 + 1.346 * (first_letter + last_letter)
speed_rad = speed_rpm * 2 * math.pi / 60

# Dimensions - inches
normal_diameter = 1.5
o_diameter = 10
c_diameter = 20
d_diameter = 20

point_a = 0.5
point_o = 6.5
point_c = 14
point_d = 20
point_e = 24
point_b = 24.5

# Material Properties - kpsi
uts = 116
sy = 96

# Forces - lbs
o_weight = 35
c_weight = 35
d_weight = 35

Ft = (1 / (4 * speed_rad * (o_diameter / 2))) * power_torque # Fz
Fa = Ft * 6/14 # Fx
Fr = Ft * 7/14 # Fy

Pt = (1 / (speed_rad * (c_diameter / 2))) * power_torque # Pz
Pr = math.tan(20 * math.pi / 180) * Pt # Py

Lt = (3 / (4 * speed_rad * (d_diameter / 2))) * power_torque # Lz
Lr = math.tan(20 * math.pi / 180) * Lt # Ly

## Reaction Forces
Ay = (1 / (point_b - point_a)) * (Fa * (o_diameter / 2) - Fr * (point_b - point_o) + Pr * (point_b - point_c) - Lr * (point_b - point_d) + d_weight * (point_b - point_d) + c_weight * (point_b - point_c) + o_weight * (point_b - point_o))
By = Pr - Fr - Lr - Ay + d_weight + c_weight + o_weight

Az = (1 / (point_b - point_a)) * (Fr * (point_b - point_o) + Pr * (point_b - point_c) + Lr * (point_b - point_d))
Bz = Fr + Pr + Lr - Az

## Shear Force Diagram

# Define distances and forces
distances = [point_a, point_o, point_c, point_d, point_b]
# Calculate forces at each point
forces_xy = [
    Ay,
    Ay - o_weight + Fr,
    Ay - o_weight + Fr - c_weight - Pr,
    Ay - o_weight + Fr - c_weight - Pr - d_weight + Lr,
    Ay - o_weight + Fr - c_weight - Pr - d_weight + Lr + By
]
forces_xz = [
	Az,
	Az - Fr,
	Az - Fr - Pr,
	Az - Fr - Pr - Lr,
	Az - Fr - Pr - Lr + Bz 
]

# Add starting and ending points
distances = [0] + distances + [25]
forces_xy = [0] + forces_xy + [0]
forces_xz = [0] + forces_xz + [0]

# Calculate bending moments
new_distances = [0]
moments_xy = [0]
moments_xz = [0]

for i in range(1, len(distances)):
	moment_xy = moments_xy[-1] + forces_xy[i - 1] * (distances[i] - distances[i - 1])
	moment_xz = moments_xz[-1] + forces_xz[i - 1] * (distances[i] - distances[i - 1])

	if i == 2:  # Point O - applied moment from Fa
		new_distances.append(distances[i])  # distance before the drop
		moments_xy.append(moment_xy)  # moment before the drop

		moment_xy -= Fa * (o_diameter / 2)  # Apply the drop
		
	new_distances.append(distances[i])
	moments_xy.append(moment_xy)
	moments_xz.append(moment_xz)

# Create the plots
plt.figure()

# Shear Force Diagram - x-y plane
plt.subplot(2, 2, 1)
plt.step(distances, forces_xy, where='post', label="Shear Force", color='b')
plt.title("Shear Force Diagram (x-y plane)")
plt.xlabel("Distance (inches)")
plt.ylabel("Shear Force (lbs)")
plt.grid(True)
plt.legend()

# Bending Moment Diagram - x-y plane
plt.subplot(2, 2, 3)
plt.plot(new_distances, moments_xy, label="Bending Moment", color='r')
plt.title("Bending Moment Diagram (x-y plane)")
plt.xlabel("Distance (inches)")
plt.ylabel("Bending Moment (lb-in)")
plt.grid(True)
plt.legend()

# Shear Force Diagram - x-z plane
plt.subplot(2, 2, 2)
plt.step(distances, forces_xz, where='post', label="Shear Force", color='b')
plt.title("Shear Force Diagram (x-z plane)")
plt.xlabel("Distance (inches)")
plt.ylabel("Shear Force (lbs)")
plt.grid(True)
plt.legend()

# Bending Moment Diagram - x-z plane
plt.subplot(2, 2, 4)
plt.plot(distances, moments_xz, label="Bending Moment", color='r')
plt.title("Bending Moment Diagram (x-z plane)")
plt.xlabel("Distance (inches)")
plt.ylabel("Bending Moment (lb-in)")
plt.grid(True)
plt.legend()

# Show the plots
plt.tight_layout()
plt.show()