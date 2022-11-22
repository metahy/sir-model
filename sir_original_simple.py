import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt


# model
def SIR_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return ([dS_dt, dI_dt, dR_dt])


# initialization

S0 = 0.9 # ratio
I0 = 0.1 # ratio
R0 = 0.0 # ratio
beta = 0.35
gamma = 0.1

# time vector
t = np.linspace(0, 100, 100)
# result
res = scipy.integrate.odeint(SIR_model, [S0, I0, R0], t, args=(beta, gamma))
print(res)
res = np.array(res)
print(res)
# plot
plt.figure(figsize=[6, 4])
plt.plot(t, res[:, 0], label='S(t)')
plt.plot(t, res[:, 1], label='I(t)')
plt.plot(t, res[:, 2], label='R(t)')
plt.legend()
plt.grid()
plt.xlabel('time')
plt.ylabel('proportions')
plt.title('SIR model simulation')
plt.show()