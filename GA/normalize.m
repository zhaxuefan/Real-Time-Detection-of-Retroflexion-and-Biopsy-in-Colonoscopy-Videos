nf = f(:,1:21);
max_v = max(nf);%1*19
min_v = min(nf);%1*19
norm_f = (f(:,1:21)-min_v)./(max_v - min_v);
norm_f(:,22) = f(:,22);
% for i = 1:length(m)
%     normalized_m(i,1:19) = (m(i,1:19) - min_v)/(max_v - min_v);
% end
    