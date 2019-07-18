X = f(:,1:19);
[n,d] = size(X);

%form RBF over the data:
nms = sum(X'.^2);
K = exp(-nms'*ones(1,n) -ones(n,1)*nms + 2*X*X');