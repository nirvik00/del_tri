import rhinoscriptsyntax as rs
import random
import math
import operator
from operator import itemgetter
import os

def genPts():
    pts=[]
    pt_li=[]
    for i in range(7):
        x=random.randint(0,100)
        y=random.randint(0,100)
        z=random.randint(0,0)
        p=[x,y,z]
        pt=rs.AddPoint(p)
        pts.append(pt)
        rs.AddTextDot(i,pt)
    initDelauney(pts)
    
def initDelauney(pts):
    tri_li=[]
    for i in pts:
        this_li=[]
        for j in pts:
            if(rs.Distance(i,j)>0):
                for k in pts:
                    if(rs.Distance(i,k)>0 and rs.Distance(j,k)>0):
                        this_li=checkIter(i,j,k,pts,tri_li)
                        if(this_li is not None):
                            tri_li.append(this_li)
                        
    print(len(tri_li))
    for m in tri_li:
        a=rs.coerce3dpoint(m[0])
        b=rs.coerce3dpoint(m[1])
        c=rs.coerce3dpoint(m[2])
        try:
            T=angDP(a,b,c)
            if(T==True):
                poly2=rs.AddPolyline([a,b,c,a]) # tri from tri_li
                pl_srf=rs.AddPlanarSrf(poly2)
                rs.ObjectColor(pl_srf,(150,10,10))
        except:
            print('error',a,b,c)

def angDP(a,b,c):
    L1=rs.AddLine(a,b)
    L2=rs.AddLine(b,c)
    L3=rs.AddLine(c,a)
    ang_b=rs.Angle2(L1,L2)
    ang_c=rs.Angle2(L2,L3)
    rs.DeleteObjects([L1,L2,L3])
    if(ang_b<20 or ang_b>135 or ang_c<20 or ang_c>135):
        #return False # dont draw
        return True        
    else:
        return True
    
def checkIter(i,j,k,pts,tri_li):
    cir=rs.AddCircle3Pt(i,j,k)
    cen=rs.CircleCenterPoint(cir)
    d=rs.Distance(cen,i)
    ar=rs.CurveArea(cir)[0]
    # 1. no other point is inside this circle
    sum=0
    for m in pts:
        d2=rs.Distance(m,cen)
        if(d2<d):
            sum+=1
    if(sum<1):
        # if there is nothing in the list add 
        if(len(tri_li)==0):
            rs.DeleteObject(cir)
            return([i,j,k])
        # else if the polygon exists do not add
        else:
            sum2=0
            for n in tri_li:
                a=n[0]
                b=n[1]
                c=n[2]
                cir2=rs.AddCircle3Pt(a,b,c)
                cen2=rs.CircleCenterPoint(cir2)
                d2=rs.Distance(cen2,cen)
                ar2=rs.CurveArea(cir2)[0]
                rs.DeleteObject(cir2)
                if(math.fabs(ar2-ar)<1):
                    sum2+=1
            if(sum2<1):
                rs.DeleteObject(cir)    
                return [i,j,k]
            else:
                rs.DeleteObject(cir)    
                return
    else:
        rs.DeleteObject(cir)    
        return
    
                    

genPts()