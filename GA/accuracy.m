
% weight: 1*19
result = zeros(length(f),1)
num = 0
for i = 1:length(f)
    %if mod(i,2) ~=0
        num = num + 1;
        predict_fun = dot(weight(1:21),f(i,1:21))+weight(22);
        result(i,:) = predict_fun;
end
%         if trainingData(len,:) == 0 
%             break
%         end
        correct_num = 0;
%         class1 = abs(norm_result - 0);
%         class2 = abs(norm_result - 1);
        predict_result = zeros(length(f),1);
        for i = 3646:4413
            if result(i) < 0
                predict_result(i) = -1;
            else
                predict_result(i) = 1;
            end
            if predict_result(i) == f(i,22)
                correct_num = correct_num + 1;
            end
        end
%         if predict_result == f(i,20)
%             correct_num = correct_num + 1;
%         end


%% machine learning predict
correct_num = 0;
yfit = trainedModel1.predictFcn(f(:,1:21));
for i = 2401:3086
    if yfit(i) == f(i,22)
                correct_num = correct_num + 1;
    end
end
    