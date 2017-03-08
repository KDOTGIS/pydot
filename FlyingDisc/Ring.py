'''
Created on Oct 19, 2016

stolen from equations for the aerboie flying disc
http://www.aerobie.narod.ru/aerobie.htm
Alan Adler - Superflight Inc, Palo Alto, CA


@author: kyleg
'''

if __name__ == '__main__':
    pass

def main():
    AerobieTest()

def AerobieTest():
       
    class params:
        #Units in inches
        #Dimensions of aerobie (inches)
        OuterDiameter = 13
        InnerDiameter = 10
        
    OD = params.OuterDiameter
    ID = params.InnerDiameter
    
    #Aspect ratio of each half-ring taken separately
    AR = ID/(0.5*(OD-ID))
    print AR
    
    #Lift slope (CL/Deg) of half-ring
    a = 0.11/(1+(2/AR))
    print a
    
    #A typical range of attack angle alpha,  Greater aplha occurs at the end of the flight.
    alpha = [2, 4, 6, 8, 10]
    
    for aoa in alpha:
        #Lift coefficient of leading ring
        CL1 = a*(aoa)
        
        
        #approximate downwash angle in degrees due to hte leading half ring at the location of the trailing half ring
        e = 36*(CL1/AR) 
        
        #angle of attack at trailing half ring
        alpha2 = aoa-e  
        
        #Lift coefficient of trailing half ring
        CL2 = alpha2*a
        
        
        #Ratio of Lift Coefficients at half rings
        #Note that R is constant at all values of a. The actual ratio may be even lower because the leading half-ring has greater leading edge span than the trailing half-ring.
        
        R = CL2/CL1
        print aoa, e, CL1, CL2, R
    
    #alan states:  ... 
    #I continued to seek a design which would remain balanced, and thus fly straight, over a range of speeds. 
    #In spinning flight, the flow direction over the ring's section reverses for half of every revolution of spin.
    # It occurred to me that if the ratio of section lift slopes (CL/a) for normal and reversed flow were 1:0.54, 
    #downwash effects would be compensated and balance would be achieved. I directed my efforts at the design of such a section.
    #...
    # continued to seek a design which would remain balanced, and thus fly straight, over a range of speeds. 
    #In spinning flight, the flow direction over the ring's section reverses for half of every revolution of spin. 
    #It occurred to me that if the ratio of section lift slopes (CL/a) for normal and reversed flow were 1:0.54, 
    #downwash effects would be compensated and balance would be achieved. 
    #I directed my efforts at the design of such a section.
    
    #I tried several other (unsuccessful) designs before returning to the reflexed concept. 
    #My next section had a filled-in area under the reflex to establish the Kutta condition at a level lower than the leading edge stagnation point 
    #and thus produce adequate lift for normal flow. It also had a much more severe reflex, more like a spoiler.
    #Flight tests quickly showed that this was the design I had been seeking. The ring was exceptionally stable over a wide range of speeds.
    #The last step was to optimize the section. I experimented with design variations in the section profile, the spoiler, and the flap. 
    #About a dozen rings were tested and the one exhibiting the best combination of stability and low drag was selected for production. 
    #The selected section even remained balanced in stall.
    #Although my intent with this section design was to reduce the lift slope for reversed flow, 
    #it is quite likely that the thick trailing edge also increases the lift slope for normal flow. 
    #The important thing is that the ratio of the lift slopes (for normal and reversed flow) be great enough to compensate for downwash and provide balanced flight.
    #While the "spoiler" slightly increases the section drag, 
    #its contribution to stability is so beneficial that overall performance is much better than the earlier conical design. 
    #An Aerobie has been thrown 1,257 feet -- a new Guinness record.


import pandas as pd

import numpy as np

import matplotlib.pyplot as plt



    
main()