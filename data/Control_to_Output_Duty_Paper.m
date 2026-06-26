clear;

% Input parameters are defined
s = tf('s');
% mDuty = [ 0.361, 0.185 ];
% SwitchingFrequency = [ 1.05, 1.05 ];
% mR = [ 5, 20 ];
% mInput = [ 2, 2 ]; % 1:Vg 2:D 3:Ws 4:Io

mDuty = [ 0.361, 0.185 ];
SwitchingFrequency = [ 1.05, 1.05 ];
mR = [ 5, 20 ];
mInput = [ 2, 2 ]; % 1:Vg 2:D 3:Ws 4:Io
C = 51*10^-9;
L = 197*10^-6;
C_f = 32*10^-6;
r_s = 1e-3;
r_c = 1e-3;
V_o = 200;
V_g = 400;
Output = 1; % 1:Vo 2:Ig
mTxtInput = ["Vg", "D", "W", "io"];

for i = 1:1:size(SwitchingFrequency, 2)
    % Load transfer function
    cal_parameter_APWM(mDuty(1, i), SwitchingFrequency(1, i), mR(1, i), r_s, r_c, C, L, C_f, V_g, mInput(1, i), Output);
    load("nData.mat");
    G_APWM(1, i) = G;
end

%% Plot Section
cColor = [ "r", "b", "m", "c", "g", "k"];

% Bodeplot function options settings
optsBodeplot_1 = bodeoptions;
optsBodeplot_1.FreqUnits = 'Hz';
optsBodeplot_1.Grid = 'On';

% Plecs gain bodeplot plot
figure(Name=("Bodeplot"));
for i = 1:1:size(SwitchingFrequency, 2)
    cFileName = ".\Plecs Data\1\CCM_" + mTxtInput(1, mInput(1, i)) +"_APWM_D" + mDuty(1, i) + "_F" + SwitchingFrequency(1, i) + "_R" + mR(1, i) + "_Vo" + V_o + ".csv";
    mData = readmatrix(cFileName);
    cLegendName = (" Plecs Simulation Fs=Fo×" + SwitchingFrequency(1, i) + "/Duty=" + mDuty(1, i) + "/Load Resistor=" + mR(1, i));
    plot(mData(:, 1), mData(:, 2), ("-." + cColor(1, i)), LineWidth=2, DisplayName=cLegendName);
    hold on;
end
legend show;

% Transfer function plot
for i = 1:1:size(SwitchingFrequency, 2)
    cLegendName(1, i) = (" Matlab Fs=Fo×" + SwitchingFrequency(1, i) + "/Duty=" + mDuty(1, i) + "/Load Resistor=" + mR(1, i));
    B_G_vd = bodeplot(G_APWM(1, i), ("--*" + cColor(1, i)), ...
        {10e1 10e5}, optsBodeplot_1);
end
legend(cLegendName);

% Plecs phase bodeplot plot
for i = 1:1:size(SwitchingFrequency, 2)
    cFileName = ".\Plecs Data\1\CCM_" + mTxtInput(1, mInput(1, i)) +"_APWM_D" + mDuty(1, i) + "_F" + SwitchingFrequency(1, i) + "_R" + mR(1, i) + "_Vo" + V_o + ".csv";
    mData = readmatrix(cFileName);
    mData(:, 3) = mData(:, 3) + 0;
    cLegendName = (" Plecs Simulation Fs=Fo×" + SwitchingFrequency(1, i) + "/Duty=" + mDuty(1, i) + "/Load Resistor=" + mR(1, i));
    plot(mData(:, 1), mData(:, 3), ("-." + cColor(1, i)), LineWidth=2, DisplayName=cLegendName);
end
hold off;