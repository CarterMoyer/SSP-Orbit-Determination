# OD2
# distance of bus
from time import sleep

def drt_bus(t):
    x_bus = 65 * t
    return x_bus

# distance of batmobile
def drt_bm(t):
    x_bm = 85 * (t - 6/60)
    return x_bm
    
def drt(step):
    t = 0
    batmobile = drt_bm(0)
    bus = drt_bus(0)
    counter = 1
    tiny = step # sets tiny = to step size
    itermax = 10000
    while (batmobile - bus) <= tiny: # checks to see the difference between distances
        t += step
        batmobile = drt_bm(t)
        bus = drt_bus(t)
        counter += 1
        if counter > itermax:
            print('Let me in.')
            sleep(2)
            print('LET ME INNNNNNN!') # Oh our lord, Bradely, forgive me
            sleep(3)
            print('Turns exceeded, aborting procedure')
            break
    if counter < itermax: # ensures the print statements are not done after itermax
        print(t * 60, 'minutes')
        print(counter, 'th iteration')
        print('Distance of bus: ', bus)
        print('Distance of batmobile: ', batmobile)

drt(10**-3)
