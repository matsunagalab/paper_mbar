C = getconstants();
KB = C.KB;
KBT = KB*300; % KB is the Boltzmann constant in kcal/(mol K)

K = 20;
temperature = [300.00 302.53 305.09 307.65 310.24 312.85 315.47 ...
               318.12 320.78 323.46 326.16 328.87 331.61 334.37 337.14 339.94 342.75 345.59 348.44 351.26]; 

u_k = [];
for k = 1:K
  f = sprintf('../4_sort_dcd/remd_paramID%d.pot', k);
  d = load(f);
  u_k = [u_k d(:,2)];
end

%% evaluate u_kl: reduced bias-factor or potential energy of umbrella simulation data k evaluated by umbrella l
for k = 1:K
  for l = 1:K
    u_kl{k, l} = u_k(:, k) ./ (KB * temperature(l));
  end
end

%% MBAR
% calculate free energies of umbrella systems
f_k = mbar(u_kl);

for k = 1:K
  u_k2{k} = u_kl{k, 1};
end

[~, w_k] = mbarpmf(u_kl, [], f_k, u_k2);

weight = [];
for k = 1:K
  weight = [weight w_k{k}];
end

%% save
save -v7.3 analyze.mat;

