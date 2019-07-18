
% weight: 1*19
result = zeros(length(f),1)
num = 0
for i = 1:length(f)
    %if mod(i,2) ~=0
        num = num + 1;
        predict_fun = dot(weight(1:19),f(i,1:19))+weight(20);
        result(i,:) = predict_fun;
end
%         if trainingData(len,:) == 0 
%             break
%         end
        correct_num = 0;
%         class1 = abs(norm_result - 0);
%         class2 = abs(norm_result - 1);
        predict_result = zeros(length(f),1);
        for i = 1:length(f)
            if result(i) <-12
                predict_result(i) = -1;
            else
                predict_result(i) = 1;
            end
            if predict_result(i) == f(i,20)
                correct_num = correct_num + 1;
            end
        end
%         if predict_result == f(i,20)
%             correct_num = correct_num + 1;
%         end
    