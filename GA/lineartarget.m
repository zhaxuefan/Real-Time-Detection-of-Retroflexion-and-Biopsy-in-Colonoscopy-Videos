
    
function loss = lineartarget(weight)

load('feature.mat');
loss = 0
for i =1:length(f)
    if f(i,22) * (dot(weight(1:21),f(i,1:21))+weight(22)) < 0
        loss = loss + 1;
    end
end
% function loss = lineartarget(weight)
% loss = 1/2 * dot(weight',weight);  
% end