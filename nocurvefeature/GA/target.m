% MATLAB��GA����ֻ������(����)��Сֵ����Ҫ��Ŀ�꺯��ȡ��
function g = target(w)
m = load('normalizedfeature.mat');
f = m.f;
feature = f(:,1:19);
label = f(:,20);
g = sum(abs(label - logsig(feature * w)));
end

    
