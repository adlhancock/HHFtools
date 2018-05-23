# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 22:29:24 2016

@author: David
"""

def htc(coolant,geometry):
    """
    Definition:
        
    Ref:
       "Heat transfers from pin-fin arrays 
       experiencing forced convection" 
       Applied Energy 67 (2000) 419-442
    Range of validity:
        
    """

    def Nu(coolant,
            geometry):

#        assert coolant._type == "air", "coolant is of type {}".format(coolant._type)
 
       
        Sx = geometry.pinarrangement.sx
        Sy = geometry.pinarrangement.sy
        Wb = geometry.channelwidth
        L = geometry.length
        alignment =  geometry.pinarrangement.alignment
        Re = coolant.Reynolds(geometry.D_h)
#       Re = 100000
        """
        #Ref:
        #"Heat transfers from pin-fin arrays 
        #experiencing forced convection" 
        #Applied Energy 67 (2000) 419-442
       
        XX = Sx / Wb
        YY = Sy /L 

        regressionterms = {"inline":[9.02e-3, 
                                     1.011,
                                     0.285,
                                     0.212],
                            "staggered":[7.04e-3,
                                         0.953,
                                         0.091,
                                         0.053]}
                            
        validlimits = {"inline":[0.004,0.332,0.033,0.212],
                       "staggered":[0.004,0.332,0.033,0.152]}
                       
        
        a, b, c, d = regressionterms[alignment]
        u,v,w,x = validlimits[alignment]
        
        
        assert all((u <= XX <= v, w <= YY <= x)), "geometry not valid"
    
        Nu = a * Re**b * XX**c * YY**d
        """
        
        return Nu
    
    
    
    Nu = Nu(coolant,geometry)
    k = coolant.k
    D_h = geometry.D_h
    return Nu * k / D_h
    



