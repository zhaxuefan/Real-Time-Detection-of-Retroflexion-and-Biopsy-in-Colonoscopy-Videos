% MATLAB的GA工具只求函数的(近似)最小值，需要将目标函数取反
function g = target(w)
m = load('normalizedfeature.mat');
f = m.f;
feature = f(:,1:19);
label = f(:,20);
g = sum(abs(label - logsig(feature * w)));
end

    
