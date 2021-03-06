prologues := 3;

input TEX;


vardef real_curve(expr a, b, xmin, xmax, ymin, ymax, dx) =
    picture result; result = nullpicture;
    for x = xmin step dx until xmax:
        numeric xa; xa = x - dx/2;
        numeric xb; xb = x + dx/2;
        numeric ka; ka = xa*xa*xa + a*xa + b;
        numeric kb; kb = xb*xb*xb + a*xb + b;
        if (ka >= 0) and (kb >= 0):
            numeric ya; ya = sqrt(ka);
            numeric yb; yb = sqrt(kb);
            if (xmin <= xa) and (xb <= xmax):
                if (ymin <= +ya) and (+ya <= ymax) and (ymin <= +yb) and (+yb <= ymax):
                    addto result doublepath (xa*u,+ya*u)--(xb*u,+yb*u);
                fi;
                if (ymin <= -ya) and (-ya <= ymax) and (ymin <= -yb) and (-yb <= ymax):
                    addto result doublepath (xa*u,-ya*u)--(xb*u,-yb*u);
                fi;
            fi;
        fi;
        if (ka >= 0) and (kb < 0):
            numeric ya; ya = sqrt(ka);
            if (xmin <= xa) and (ymin <= -ya) and (ya <= ymax):
                addto result doublepath (xa*u,-ya*u)--(xa*u,+ya*u);
            fi;
        fi;
        if (ka < 0) and (kb >= 0):
            numeric yb; yb = sqrt(kb);
            if (xb <= xmax) and (ymin <= -yb) and (yb <= ymax):
                addto result doublepath (xb*u,-yb*u)--(xb*u,+yb*u);
            fi;
        fi;
    endfor;
    result
enddef;

vardef finite_curve(expr a, b, p, xmin, xmax, ymin, ymax) =
    picture result; result = nullpicture;
    for x = ceiling(xmin) step 1 until floor(xmax):
        for y = ceiling(ymin) step 1 until floor(ymax):
            if (x*x*x + a*x + b) mod p = (y*y) mod p:
                addto result doublepath (x*u, y*u)--cycle;
            fi;
        endfor;
    endfor;
    result
enddef;

vardef xgrid(expr xmin, xmax, ymin, ymax, spacing, offset) =
    picture result; result = nullpicture;
    numeric xfirst; xfirst = ceiling((xmin-offset)/spacing)*spacing+offset;
    numeric xlast; xlast = floor((xmax-offset)/spacing)*spacing+offset;
    for x = xfirst step spacing until xlast:
        addto result doublepath (x*u, ymin*u)--(x*u, ymax*u);
    endfor;
    result
enddef;

vardef ygrid(expr xmin, xmax, ymin, ymax, spacing, offset) =
    picture result; result = nullpicture;
    numeric yfirst; yfirst = ceiling((ymin-offset)/spacing)*spacing+offset;
    numeric ylast; ylast = floor((ymax-offset)/spacing)*spacing+offset;
    for y = yfirst step spacing until ylast:
        addto result doublepath (xmin*u, y*u)--(xmax*u, y*u);
    endfor;
    result
enddef;

vardef xaxis(expr xmin, xmax, length) =
    path result; result = (xmin*u, 0*u)--(xmax*u+length, 0*u);
    result
enddef;

vardef yaxis(expr ymin, ymax, length) =
    path result; result = (0*u, ymin*u)--(0*u, ymax*u+length);
    result
enddef;

vardef xscale(expr xmin, xmax, spacing, offset, length) =
    picture result; result = nullpicture;
    numeric xfirst; xfirst = ceiling((xmin-offset)/spacing)*spacing+offset;
    numeric xlast; xlast = floor((xmax-offset)/spacing)*spacing+offset;
    for x = xfirst step spacing until xlast:
        addto result doublepath (x*u, 0*u)--(x*u, -length);
    endfor;
    result
enddef;

vardef yscale(expr ymin, ymax, spacing, offset, length) =
    picture result; result = nullpicture;
    numeric yfirst; yfirst = ceiling((ymin-offset)/spacing)*spacing+offset;
    numeric ylast; ylast = floor((ymax-offset)/spacing)*spacing+offset;
    for y = yfirst step spacing until ylast:
        addto result doublepath (0*u, y*u)--(-length, y*u);
    endfor;
    result
enddef;

vardef originlabel =
    picture result; result = thelabel.llft(btex $0$ etex, (0*u, 0*u));
    result
enddef;

vardef xlabel(expr xmin, xmax, spacing, offset) =
    picture result; result = nullpicture;
    numeric xfirst; xfirst = ceiling((xmin-offset)/spacing)*spacing+offset;
    numeric xlast; xlast = floor((xmax-offset)/spacing)*spacing+offset;
    for x = xfirst step spacing until xlast:
        addto result also thelabel.llft(TEX("$" & decimal(x) & "$"), (x*u, 0*u));
    endfor;
    result
enddef;

vardef ylabel(expr ymin, ymax, spacing, offset) =
    picture result; result = nullpicture;
    numeric yfirst; yfirst = ceiling((ymin-offset)/spacing)*spacing+offset;
    numeric ylast; ylast = floor((ymax-offset)/spacing)*spacing+offset;
    for y = yfirst step spacing until ylast:
        addto result also thelabel.llft(TEX("$" & decimal(y) & "$"), (0*u, y*u));
    endfor;
    result
enddef;


outputtemplate := "elliptic_curves_%c.mps";

beginfig(1);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel shifted (-0.05u, -0.05u);
    draw xlabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw xlabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw real_curve(-1, 1, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;
endfig;

beginfig(2);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(+1, +2, 1.0, 0.0);
    draw xlabel(-1, -1, 1.0, 0.0);
    draw ylabel(+1, +2, 1.0, 0.0);
    draw ylabel(-1, -1, 1.0, 0.0);
    draw real_curve(-1, 0, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;
endfig;

beginfig(3);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(+1, +2, 1.0, 0.0);
    draw xlabel(-1, -1, 1.0, 0.0);
    draw ylabel(+1, +2, 1.0, 0.0);
    draw ylabel(-1, -1, 1.0, 0.0);
    draw real_curve(0, -1, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;
endfig;

beginfig(4);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(+1, +2, 1.0, 0.0);
    draw xlabel(-1, -1, 1.0, 0.0);
    draw ylabel(+1, +2, 1.0, 0.0);
    draw ylabel(-1, -1, 1.0, 0.0);
    draw real_curve(-3, 2, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;
endfig;

beginfig(5);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(+1, +2, 1.0, 0.0);
    draw xlabel(-1, -1, 1.0, 0.0);
    draw ylabel(+1, +2, 1.0, 0.0);
    draw ylabel(-1, -1, 1.0, 0.0);
    draw real_curve(0, 0, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;
endfig;

beginfig(6);
    numeric u; u = 0.333cm;

    draw xgrid(0, 12, 0, 12, 1.0, 0.0) dashed dashpattern(on 0 off 1u) withpen pencircle scaled 0.25pt;
    draw ygrid(0, 12, 0, 12, 1.0, 0.0) dashed dashpattern(on 0 off 1u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(0, 12, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(0, 12, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(0, 12, 3.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(0, 12, 1.0, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(0, 12, 3.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(0, 12, 1.0, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(1, 12, 3.0, 0.0);
    draw ylabel(1, 12, 3.0, 0.0);
    draw finite_curve(2, 6, 13, 0, 12, 0, 12) withpen pencircle scaled 4pt;
endfig;

beginfig(7);
    numeric u; u = 0.333cm;

    draw xgrid(0, 12, 0, 12, 1.0, 0.0) dashed dashpattern(on 0 off 1u) withpen pencircle scaled 0.25pt;
    draw ygrid(0, 12, 0, 12, 1.0, 0.0) dashed dashpattern(on 0 off 1u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(0, 12, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(0, 12, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(0, 12, 3.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(0, 12, 1.0, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(0, 12, 3.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(0, 12, 1.0, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel;
    draw xlabel(1, 12, 3.0, 0.0);
    draw ylabel(1, 12, 3.0, 0.0);
    draw finite_curve(7, 3, 13, 0, 12, 0, 12) withpen pencircle scaled 4pt;
endfig;


outputtemplate := "elliptic_curve_groups_%c.mps";

beginfig(1);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel shifted (-0.05u, -0.05u);
    draw xlabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw xlabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);

    numeric a; a = -3;
    numeric b; b = +1.5;

    draw real_curve(a, b, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;

    x1 = -1.75;
    y1 = sqrt(x1*x1*x1 + a*x1 + b);

    draw (x1*u, y1*u)--cycle withpen pencircle scaled 4pt;

    label.lrt(btex $P$ etex, (x1*u, y1*u));
endfig;

beginfig(2);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel shifted (-0.05u, -0.05u);
    draw xlabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw xlabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);

    numeric a; a = -3;
    numeric b; b = +1.5;

    draw real_curve(a, b, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;

    x1 = -1.75;
    y1 = sqrt(x1*x1*x1 + a*x1 + b);

    draw (x1*u, y1*u)--cycle withpen pencircle scaled 4pt;
    draw (x1*u, -y1*u)--cycle withpen pencircle scaled 4pt;

    label.lrt(btex $P$ etex, (x1*u, y1*u));
    label.urt(btex $\overline{P}$ etex, (x1*u, -y1*u));

    draw (x1*u,-2u)--(x1*u,2u) dashed dashpattern(off 0.05u on 0.15u off 0.05u) withpen pencircle scaled 0.75pt;
endfig;

beginfig(3);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel shifted (-0.05u, -0.05u);
    draw xlabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw xlabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);

    numeric a; a = -3;
    numeric b; b = +1.5;

    draw real_curve(a, b, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;

    x1 = -1.75;
    y1 = sqrt(x1*x1*x1 + a*x1 + b);
    x2 = +0.25;
    y2 = sqrt(x2*x2*x2 + a*x2 + b);

    numeric lambda; lambda = (y2 - y1)/(x2 - x1);

    x3 = lambda*lambda - x2 - x1;
    y3 = -lambda*(x3 - x1) - y1;

    draw (x1*u, y1*u)--cycle withpen pencircle scaled 4pt;
    draw (x2*u, y2*u)--cycle withpen pencircle scaled 4pt;
    draw (x3*u, y3*u)--cycle withpen pencircle scaled 4pt;
    draw (x3*u, -y3*u)--cycle withpen pencircle scaled 4pt;

    label.lrt(btex $P$ etex, (x1*u, y1*u));
    label.urt(btex $Q$ etex, (x2*u, y2*u));
    label.llft(btex $R$ etex, (x3*u, y3*u));
    label.ulft(btex $\overline{R}$ etex, (x3*u, -y3*u));

    x4 = -2;
    z4 = whatever[z1,z2];
    x5 = 2;
    z5 = whatever[z1,z2];
    draw (z4*u)--(z5*u) dashed dashpattern(off 0.05u on 0.15u off 0.05u) withpen pencircle scaled 0.75pt;
    draw (x3*u,-2u)--(x3*u,2u) dashed dashpattern(off 0.05u on 0.15u off 0.05u) withpen pencircle scaled 0.75pt;
endfig;

beginfig(4);
    numeric u; u = 1cm;

    draw xgrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    draw ygrid(-2, +2, -2, +2, 1.0, 0.0) dashed dashpattern(on 0.0005u off 0.099u on 0.0005u) withpen pencircle scaled 0.25pt;
    drawarrow xaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    drawarrow yaxis(-2, 2, 0.25cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw xscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 1.0, 0.0, 0.15cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.5, 0.0, 0.10cm) withpen pencircle scaled 0.5pt;
    draw yscale(-2, +2, 0.1, 0.0, 0.05cm) withpen pencircle scaled 0.5pt;
    draw originlabel shifted (-0.05u, -0.05u);
    draw xlabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw xlabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(+1, +2, 1.0, 0.0) shifted (-0.05u, -0.05u);
    draw ylabel(-1, -1, 1.0, 0.0) shifted (-0.05u, -0.05u);

    numeric a; a = -3;
    numeric b; b = +1.5;

    draw real_curve(a, b, -2, +2, -2, +2, 0.001) withpen pencircle scaled 1pt;

    x1 = 0.0;
    y1 = sqrt(x1*x1*x1 + a*x1 + b);

    numeric lambda; lambda = (3*x1*x1 + a)/(2*y1);

    x2 = lambda*lambda - 2*x1;
    y2 = -lambda*(x2 - x1) - y1;

    draw (x1*u, y1*u)--cycle withpen pencircle scaled 4pt;
    draw (x2*u, y2*u)--cycle withpen pencircle scaled 4pt;
    draw (x2*u, -y2*u)--cycle withpen pencircle scaled 4pt;

    label.urt(btex $P$ etex, (x1*u, y1*u));
    label.ulft(btex $Q$ etex, (x2*u, y2*u));
    label.llft(btex $\overline{Q}$ etex, (x2*u, -y2*u));

    y3 = 2;
    z3 = whatever[(x1,y1),(x2,-y2)];
    x4 = 2;
    z4 = whatever[(x1,y1),(x2,-y2)];
    draw (z3*u)--(z4*u) dashed dashpattern(off 0.05u on 0.15u off 0.05u) withpen pencircle scaled 0.75pt;
    draw (x2*u,-2u)--(x2*u,2u) dashed dashpattern(off 0.05u on 0.15u off 0.05u) withpen pencircle scaled 0.75pt;
endfig;


end.
