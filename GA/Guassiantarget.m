function loss = Guassiantarget(weight)

load('train.mat');
loss = 0
for i =1:length(f)
    if f(i,20) * (dot(weight(1:19),f(i,1:19))+weight(20)) < 0
        loss = loss + 1;
    end
end