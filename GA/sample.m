f1_1 = zeros(2014,20);
f1_2 = zeros(2015,20);
for i = 1:length(f2)
    if mod(i,2) == 0
        f2_1(i/2,:) = f2(i,:);
    else
        f2_2((i+1)/2,:) = f2(i,:);
    end
end