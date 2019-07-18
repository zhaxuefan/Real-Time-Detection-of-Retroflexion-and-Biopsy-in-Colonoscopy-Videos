max_v = max(result(:));%1*19
min_v = min(result(:));%1*19
normalized_result = (result-min_v)/(max_v - min_v);
% for i = 1:length(m)
%     normalized_m(i,1:19) = (m(i,1:19) - min_v)/(max_v - min_v);
% end
    