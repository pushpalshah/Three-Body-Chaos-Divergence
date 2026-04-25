import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ==========================================
# 1. THE GRAVITY ENGINE
# ==========================================
G = 4 * np.pi**2
masses = np.array([1.0, 1.0, 1.0]) # Three stars of equal mass
num_bodies = 3

def three_body_equations(t, state):
    """Calculates the forces for the 3-body system."""
    positions = state[:2 * num_bodies].reshape((num_bodies, 2))
    velocities = state[2 * num_bodies:].reshape((num_bodies, 2))
    accelerations = np.zeros_like(positions)
    
    for i in range(num_bodies):
        for j in range(num_bodies):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_sq = np.sum(r_vec**2)
                accelerations[i] += G * masses[j] * r_vec / (r_sq**1.5)
                
    return np.concatenate([velocities.flatten(), accelerations.flatten()])

# ==========================================
# 2. INITIAL CONDITIONS (Universe A vs Universe B)
# ==========================================
# Universe A: A chaotic resting start 
pos_A = np.array([[-1.0, 0.0], [1.0, 0.0], [0.0, 1.5]]) 
vel_A = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
state_A = np.concatenate([pos_A.flatten(), vel_A.flatten()])

# Universe B: Exactly the same, but Star 3 is moved by a microscopic 0.00001 AU
pos_B = np.copy(pos_A)
pos_B[2, 0] += 0.00001 # The "Butterfly Flap"
state_B = np.concatenate([pos_B.flatten(), vel_A.flatten()])

# ==========================================
# 3. RUNNING THE SIMULATIONS
# ==========================================
time_span = (0, 5) # Simulate for 5 years
time_eval = np.linspace(time_span[0], time_span[1], 5000) # High resolution

print("Simulating Universe A...")
sol_A = solve_ivp(three_body_equations, time_span, state_A, t_eval=time_eval, method='RK45', rtol=1e-9, atol=1e-9)

print("Simulating Universe B...")
sol_B = solve_ivp(three_body_equations, time_span, state_B, t_eval=time_eval, method='RK45', rtol=1e-9, atol=1e-9)

# ==========================================
# 4. CALCULATING THE DIVERGENCE 
# ==========================================
# Extract the (x,y) positions of Star 3 over time from both universes
star3_A = sol_A.y[4:6, :] 
star3_B = sol_B.y[4:6, :]

# Calculate the physical distance between Star 3 in Universe A and Star 3 in Universe B
divergence_distance = np.sqrt(np.sum((star3_A - star3_B)**2, axis=0))

# ==========================================
# 5. VISUALIZING THE CHAOS
# ==========================================
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: The Orbital Tracks
ax1.set_title("Trajectories of Star 3 (Universe A vs B)", fontsize=14)
ax1.plot(star3_A[0], star3_A[1], color='cyan', label='Universe A', linewidth=1.5, alpha=0.8)
ax1.plot(star3_B[0], star3_B[1], color='magenta', linestyle='--', label='Universe B (Shifted by 10^-5 AU)', linewidth=1.5, alpha=0.8)
ax1.set_xlabel("X Position (AU)")
ax1.set_ylabel("Y Position (AU)")
ax1.legend()
ax1.grid(alpha=0.2)

# Plot 2: The Butterfly Effect (Exponential Growth of Error)
ax2.set_title("Divergence Over Time (The Butterfly Effect)", fontsize=14)
ax2.plot(sol_A.t, divergence_distance, color='yellow', linewidth=2)
ax2.set_yscale('log') # Log scale is crucial to show exponential chaos
ax2.set_xlabel("Time (Years)")
ax2.set_ylabel("Distance Between Universes (Log Scale)")
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()
