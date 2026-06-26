function cal_parameter_APWM(Duty, F_sn, R, r_s, r_c, C, L, C_f, V_g, Input, Output)
    s = tf('s');

    Fo = 1/(2*pi*sqrt(L*C));
    Wo = 2*pi*Fo;
    Fs = F_sn*Fo;
    Ws = 2*pi*Fs;
    
    r_cc = r_c*R/(r_c+R);
    VDC = V_g*(2*Duty-1);
    V_es = V_g*2/pi*(1-cos(2*pi*Duty));
    V_ec = V_g*2/pi*sin(2*pi*Duty);
    R_e = 8/pi^2*(1-r_cc/R)*(r_c/r_cc)*R;
    
    al = 1-Ws^2*L*C;
    be = Ws*C*(R_e+r_s);
    Th = al*be/(al^2+be^2);

    V_s = ((VDC*al+VDC*be)*Th+V_es*al+V_ec*be)/(al^2+be^2);
    V_c = ((VDC*al-VDC*be)*Th+V_ec*al-V_es*be)/(al^2+be^2);

    I_s = -Ws*C*V_c;
    I_c = Ws*C*V_s;
    I_p = sqrt(I_s^2+I_c^2);
    V_cf = pi/4*I_p*R_e;
    
    k_vs = 2/pi*(1-cos(2*pi*Duty));
    k_vc = 2/pi*sin(2*pi*Duty);
    E_ds = 4*V_g*sin(2*pi*Duty);
    E_dc = 4*V_g*cos(2*pi*Duty);
    E_s = L*I_c;
    E_c = L*I_s;
    Z_s = Ws*L+4/pi*V_cf*I_s*I_c/(I_p^2)^(3/2);
    Z_c = -Ws*L+4/pi*V_cf*I_s*I_c/(I_p^2)^(3/2);
    G = Ws*C;
    k_s = 2/pi*I_s/I_p;
    k_c = 2/pi*I_c/I_p;
    J_s = C*V_c;
    J_c = C*V_s;
    R_s = r_s + 4/pi*V_cf*I_c^2/I_p^3;
    R_c = r_s + 4/pi*V_cf*I_s^2/I_p^3;
    I_d = 2*(-I_s*sin(2*pi*Duty)+I_c*cos(2*pi*Duty));
    
    %% matrix
    A = [-R_s/L, Z_s/L, -1/L, 0, -2*k_s/L, 0;
        Z_c/L, -R_c/L, 0, -1/L, -2*k_c/L, 0;
        1/C, 0, 0, G/C, 0, 0;
        0, 1/C, -G/C, 0, 0, 0;
        k_s*r_cc/(C_f*r_c), k_c*r_cc/(C_f*r_c), 0, 0, -r_cc/(R*C_f*r_c), 0;
        0, 0, 0, 0, 0, 0];

    B = [k_vs/L, E_ds/L, E_s/L, 0;
        k_vc/L, E_dc/L, -E_c/L, 0;
        0, 0, J_s/C, 0;
        0, 0, -J_c/C, 0;
        0, 0, 0, r_cc/(C_f*r_c)
        Th*(2*Duty-1), Th*V_g*2, 0, 0];

    CC = [k_s*r_cc, k_c*r_cc, 0, 0, r_cc/r_c, 0;
        1/pi*(1-cos(2*pi*Duty)), 1/pi*(sin(2*pi*Duty)), 0, 0, 0, 0];

    DD = [0, 0, 0, r_cc;
        0, I_d, 0, 0];
    %%
    
    [num, den] = ss2tf(A, B, CC, DD, Input);
    
    G = tf(num(Output, :),  den);

    save('nData.mat');
end