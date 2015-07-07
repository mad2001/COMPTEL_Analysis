# -*- coding: utf-8 -*-

def ngon(pos=(0,0), np=3, length=None, radius=1.0, rotate=0.0, thickness=0,
         roundness=0.0, invert=False, scale=1.0, xscale=1.0, yscale=1.0):
        cp = []
        if np < 3:
                raise AttributeError("number of sides can not be less than 3")
                return None

        angle = 2*pi/np
        if length != None: radius = (length/2.0)/(sin(angle/2))
        else: length = radius*(sin(angle/2))*2
        if thickness == 0:
            seg = 2.0*pi/np
            angle = rotate
            for i in range(np):
                x = radius*cos(angle) + pos[0]
                y = radius*sin(angle) + pos[1]
                cp.append((x,y))
                angle += seg
            cp.append(cp[0])
            if scale != 1.0: xscale = yscale = scale
            pp = Polygon(cp)
            if xscale != 1.0 or yscale != 1.0: pp.scale(xscale,yscale)
            if roundness > 0:
                    cp = roundc(pp.contour(0), roundness=roundness, invert=invert)
                    return Polygon(cp)
            else: return pp
        else:
            pp = nframe(pos=pos, length=length, thickness=thickness, roundness=roundness,
                        invert=invert, rotate=rotate, np=np)
            return pp

def circle(pos=(0,0), radius=0.5, np=32, scale=1.0, xscale=1.0, yscale=1.0,
            thickness=0, angle1=0, angle2=2*pi, rotate=0):
        if thickness == 0 or angle1 != 0 or angle2 != 2*pi:
            cp = []
            if angle1 != 0 or angle2 != 2*pi:
                cp.append(pos)
            seg = 2.0*pi/np
            nseg = int(abs((angle2-angle1)/seg+.5))
            seg = (angle2-angle1)/nseg
            if angle1 != 0 or angle2 != 2*pi: nseg += 1
            c = radius*cos(angle1)
            s = radius*sin(angle1)
            dc = cos(seg)
            ds = sin(seg)
            x0 = pos[0]
            y0 = pos[1]
            cp.append((x0+c,y0+s))
            for i in range(nseg-1):
                c2 = c*dc - s*ds
                s2 = s*dc + c*ds
                cp.append((x0+c2,y0+s2))
                c = c2
                s = s2
            if angle1 != 0 or angle2 != 2*pi: cp.append(cp[0])
            if rotate != 0.0 and angle1 != 0 or angle2 != 2*pi:
                cp = rotatecp(cp, pos, rotate)
            if scale != 1.0: xscale = yscale = scale
            pp = Polygon(cp)
            if xscale != 1.0 or yscale != 1.0: pp.scale(xscale,yscale)
            return pp
        else:
            if thickness == Default: thickness = radius*0.2
            pp = ring(pos=pos, radius=radius, np=np, scale=scale,
                      iradius=(radius-thickness), xscale=xscale, yscale=yscale)
            return pp