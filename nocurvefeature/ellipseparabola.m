function [c,ceq]=ellipseparabola(x)
load('train.mat');
new = f;
new(:,20) = 1;
c = - f(:,20) .* (new * x');
ceq = [];
end