# -*- coding: iso-8859-1 -*-
def cdv_SH(a,e,i):

	"""
	Compute the delta-v required to reach an asteroid with orbital parameters a, i, e, from LEO. Use unmodified formulas for unmanned missions from Shoemaker and Heilin (1979).
	a in AU, i in radians. Returns delta-V in km/s
	"""
	
	#Test case: Eros. Because Ender's Game. S & H find \delta V\approx 6.1 km/s
	import math
	#e=0.22267
	#a=1.457837 #AU
	#i=math.radians(10.82873) #degrees-->radians
	#astype='amor' #Type of asteroid: options are 'aten', 'amor', and 'apollo'. 
			#a=semimajor axis, q=perihelion distance (closest approach to sun), Q=aphelion distance (farthest approach from Sun). Definitions from Binzel et al (2002)
			#aten: a<1.0 AU, Q>0.983 AU (e.g. 1976AA)
			#amor: a>=1.0 AU, 1.017 AU<q<1.3 AU (e.g. Eros)
			#apollo: a>1.0 AU, q<=1.017 AU (e.g. Adonis)
	
	Q=(1.+e)*a #aphelion distance = maximum distance from Sun.
	q=(1.-e)*a #perihelion distance = minimum distance from Sun
	
	#if (a<1.0 and Q>0.983): #This is the Binzel way
		#astype='aten'
	#elif (a>1.0 and q<1.017):
		#astype='apollo'
	#elif (a>=1.0 and 1.017<q<1.3):
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
	#if (a<1.0): #this is the Benner way
		#astype='aten' #aten
	#elif (a>=1.0 and q<=1.0): #apollo #problem creeps in with amors and apollos. Why?
		#astype='apollo'
	#elif (a>=1.0 and q>1.0): #amor
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
		
	if (a<1.0): #this is the MPC way
		astype='aten' #aten
	elif (a>=1.0 and q<=1.0): #apollo #problem creeps in with amors and apollos. Why?
		astype='apollo'
	elif (q<=1.3 and q>1.0): #amor
		astype='amor'
	else:
		#print('Error: Asteroid type not recognized')
		astype='none'	
	
	#Initial Definitions
	#v_0=2.9785e1 #Mean orbital velocity of the Earth in km/s
	#u_0=7.784e0/v_0 #Orbital velocity at LEO, normalized from km/s to v_0. This is a fiducial quantity
	#S=1.12e1/v_0 #Escape velocity from Earth, normalized from km/s to v_0. Should also be math.sqrt(2.)*u_0 according to Jonathan's paper...which it's not quite. (0.3 km/s discrepancy). This value is right according to physics.
	
	
	##Use Benner definitions, see if it makes a difference
	v_0=2.9784e1 #Mean orbital velocity of the Earth in km/s
	u_0=7.727e0/v_0 #Orbital velocity at 400 km, normalized from km/s to v_0. 
	S=math.sqrt(2.)*u_0 #Escape velocity from Earth, normalized from km/s to v_0.
	
	if astype=='amor':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.))*math.cos(i/2.))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.)))

	elif astype=='apollo':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.)))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	elif astype=='aten':
		u_T=math.sqrt(2.-2.*math.sqrt(2.*Q-Q**2.)*math.cos(i/2.))
		u_c=math.sqrt(3./Q-1.-(2./Q)*math.sqrt(2.-Q))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	else:
		#print('Error: invalid value for astype')
		u_T=float('NaN')
		u_c=float('NaN')
		u_r=float('NaN')

	
	u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(i/2.))
	#u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(0.)) #This is fallacious Benner term
	u_L=math.sqrt(u_T**2.+S**2.)-u_0

	F=u_L+u_R
	#deltaV=F*v_0 #delta-v in km/s
	deltaV=F*30.+0.5#Use Benner way for comparison. This actually accounts for a good part of the difference. 
	
	return deltaV

def cdv_SH_bennerbug(a,e,i):

	"""
	Compute the delta-v required to reach an asteroid with orbital parameters a, i, e, from LEO. Use unmodified formulas for unmanned missions from Shoemaker and Heilin (1979).
	a in AU, i in radians. Returns delta-V in km/s
	"""
	
	#Test case: Eros. Because Ender's Game. S & H find \delta V\approx 6.1 km/s
	import math
	#e=0.22267
	#a=1.457837 #AU
	#i=math.radians(10.82873) #degrees-->radians
	#astype='amor' #Type of asteroid: options are 'aten', 'amor', and 'apollo'. 
			#a=semimajor axis, q=perihelion distance (closest approach to sun), Q=aphelion distance (farthest approach from Sun). Definitions from Binzel et al (2002)
			#aten: a<1.0 AU, Q>0.983 AU (e.g. 1976AA)
			#amor: a>=1.0 AU, 1.017 AU<q<1.3 AU (e.g. Eros)
			#apollo: a>1.0 AU, q<=1.017 AU (e.g. Adonis)
	
	Q=(1.+e)*a #aphelion distance = maximum distance from Sun.
	q=(1.-e)*a #perihelion distance = minimum distance from Sun
	
	#if (a<1.0 and Q>0.983): #This is the Binzel way
		#astype='aten'
	#elif (a>1.0 and q<1.017):
		#astype='apollo'
	#elif (a>=1.0 and 1.017<q<1.3):
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
	#if (a<1.0): #this is the Benner way
		#astype='aten' #aten
	#elif (a>=1.0 and q<=1.0): #apollo #problem creeps in with amors and apollos. Why?
		#astype='apollo'
	#elif (a>=1.0 and q>1.0): #amor
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
		
	if (a<1.0): #this is the MPC way
		astype='aten' #aten
	elif (a>=1.0 and q<=1.0): #apollo #problem creeps in with amors and apollos. Why?
		astype='apollo'
	elif (q<=1.3 and q>1.0): #amor
		astype='amor'
	else:
		print('Error: Asteroid type not recognized')
		astype='none'	
	
	#Initial Definitions
	#v_0=2.9785e1 #Mean orbital velocity of the Earth in km/s
	#u_0=7.784e0/v_0 #Orbital velocity at LEO, normalized from km/s to v_0. This is a fiducial quantity
	#S=1.12e1/v_0 #Escape velocity from Earth, normalized from km/s to v_0. Should also be math.sqrt(2.)*u_0 according to Jonathan's paper...which it's not quite. (0.3 km/s discrepancy). This value is right according to physics.
	
	
	##Use Benner definitions, see if it makes a difference
	v_0=2.9784e1 #Mean orbital velocity of the Earth in km/s
	u_0=7.727e0/v_0 #Orbital velocity at LEO, normalized from km/s to v_0. 
	S=math.sqrt(2.)*u_0 #Escape velocity from Earth, normalized from km/s to v_0.
	
	if astype=='amor':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.))*math.cos(i/2.))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.)))

	elif astype=='apollo':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.)))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	elif astype=='aten':
		u_T=math.sqrt(2.-2.*math.sqrt(2.*Q-Q**2.)*math.cos(i/2.))
		u_c=math.sqrt(3./Q-1.-(2./Q)*math.sqrt(2.-Q))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	else:
		print('Error: invalid value for astype')
		u_T=float('NaN')
		u_c=float('NaN')
		u_r=float('NaN')

	
	#u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(i/2.))
	u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(0.)) #This is fallacious Benner term
	u_L=math.sqrt(u_T**2.+S**2.)-u_0

	F=u_L+u_R
	#deltaV=F*v_0 #delta-v in km/s
	deltaV=F*30.+0.5#Use Benner way for comparison. This actually accounts for a good part of the difference. 
	
	return deltaV


def cdv_SH_400km(a,e,i):

	"""
	Compute the delta-v required to reach an asteroid with orbital parameters a, i, e, from a 400-km LEO. Use unmodified formulas for unmanned missions from Shoemaker and Heilin (1979).
	a in AU, i in radians. Returns delta-V in km/s
	"""
	
	#Test case: Eros. Because Ender's Game. S & H find \delta V\approx 6.1 km/s
	import math
	#e=0.22267
	#a=1.457837 #AU
	#i=math.radians(10.82873) #degrees-->radians
	#astype='amor' #Type of asteroid: options are 'aten', 'amor', and 'apollo'. 
			#a=semimajor axis, q=perihelion distance (closest approach to sun), Q=aphelion distance (farthest approach from Sun). Definitions from Binzel et al (2002)
			#aten: a<1.0 AU, Q>0.983 AU (e.g. 1976AA)
			#amor: a>=1.0 AU, 1.017 AU<q<1.3 AU (e.g. Eros)
			#apollo: a>1.0 AU, q<=1.017 AU (e.g. Adonis)
	
	Q=(1.+e)*a #aphelion distance = maximum distance from Sun.
	q=(1.-e)*a #perihelion distance = minimum distance from Sun
	
	#if (a<1.0 and Q>0.983): #This is the Binzel way
		#astype='aten'
	#elif (a>1.0 and q<1.017):
		#astype='apollo'
	#elif (a>=1.0 and 1.017<q<1.3):
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
	#if (a<1.0): #this is the Benner way
		#astype='aten' #aten
	#elif (a>=1.0 and q<=1.0): #apollo #problem creeps in wiLEOth amors and apollos. Why?
		#astype='apollo'
	#elif (a>=1.0 and q>1.0): #amor
		#astype='amor'
	#else:
		#print('Error: Asteroid type not recognized')
		#astype='none'	
		
	if (a<1.0): #this is the MPC way
		astype='aten' #aten
	elif (a>=1.0 and q<=1.0): #apollo #problem creeps in with amors and apollos. Why?
		astype='apollo'
	elif (q<=1.3 and q>1.0): #amor
		astype='amor'
	else:
		#print('Error: Asteroid type not recognized')
		astype='none'	
	
	#Initial Definitions
	#v_0=2.9785e1 #Mean orbital velocity of the Earth in km/s
	#u_0=7.784e0/v_0 #Orbital velocity at LEO, normalized from km/s to v_0. This is a fiducial quantity
	#S=1.12e1/v_0 #Escape velocity from Earth, normalized from km/s to v_0. Should also be math.sqrt(2.)*u_0 according to Jonathan's paper...which it's not quite. (0.3 km/s discrepancy). This value is right according to physics.
	
	
	##Use Benner definitions, see if it makes a difference
	v_0=2.9784e1 #Mean orbital velocity of the Earth in km/s
	u_0=7.668e0/v_0 #Orbital velocity at LEO, normalized from km/s to v_0. 
	S=math.sqrt(2.)*u_0 #Escape velocity from Earth, normalized from km/s to v_0.
	
	if astype=='amor':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.))*math.cos(i/2.))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.)))

	elif astype=='apollo':
		u_T=math.sqrt(3.-2./(Q+1.)-2.*math.cos(i/2.0)*math.sqrt(2.*Q/(Q+1.)))
		u_c=math.sqrt(3./Q-2./(Q+1.)-(2./Q)*math.sqrt(2./(Q+1.)))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	elif astype=='aten':
		u_T=math.sqrt(2.-2.*math.sqrt(2.*Q-Q**2.)*math.cos(i/2.))
		u_c=math.sqrt(3./Q-1.-(2./Q)*math.sqrt(2.-Q))
		u_r=math.sqrt(3./Q-1./a-(2./Q)*math.sqrt((a/Q)*(1.-e**2.))*math.cos(i/2.))
		
	else:
		#print('Error: invalid value for astype')
		u_T=float('NaN')
		u_c=float('NaN')
		u_r=float('NaN')

	
	u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(i/2.))
	#u_R=math.sqrt(u_c**2.+u_r**2.-2.*u_c*u_r*math.cos(0.)) #This is fallacious Benner term
	u_L=math.sqrt(u_T**2.+S**2.)-u_0

	F=u_L+u_R
	#deltaV=F*v_0 #delta-v in km/s
	deltaV=F*30.+0.5#Use Benner way for comparison. This actually accounts for a good part of the difference. 
	
	return deltaV