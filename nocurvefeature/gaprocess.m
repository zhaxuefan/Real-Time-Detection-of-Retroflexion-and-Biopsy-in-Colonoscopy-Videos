function GA_LS
% 基于最小方差原理的遗传算法求参数回归问题
clear all;close all;clc
  

%-------------遗传算法-----------------------------------------------------
% 使用gaoptimset函数进行参数设置
options = gaoptimset('PopulationSize',400,'Generations',800,'PlotFcn',@gaplotbestf);
% PopulationSize - 种群数量
% Generations - 遗传优化次数
% PlotFcn - 迭代过程绘图


[k1,fva,reason,output,final_pop]=ga(@lineartarget,20,[],[],[],[],[],[],@ellipseparabola,options);
load('normalizedfeature.mat');
y = Profun(k1,f); % Profun为自定义的仿真函数
figure;plot(x,y,'b-',x,Profun(k1,x),'r--');
legend('原始数据','拟合曲线');
fprintf('\n\n遗传算法的初始估计数值:\n');
fprintf('\n\t参数 a0 = %.9f',k1(1));
fprintf('\n\t参数 b0 = %.9f',k1(2));
fprintf('\n\t参数 c0 = %.9f',k1(3));
fprintf('\n\t参数 d0 = %.9f',k1(4));
end
%-------------------------------------------------------------------------

%----------------构造拟合目标函数-------------------------------------------
function loss = lineartarget(weight)
loss = 1/2 * dot(weight',weight);  
end

function [c,ceq]=ellipseparabola(x)
load('train.mat');
new = f;
new(:,20) = 1;
for i =1:length(f)
    c(i) = - f(i,20) * (dot(x,new(i,:)));
end
ceq = [];
end

%-----------------构造生成函数-----------------------------------------
function result = Profun(weight,f)

result = zeros(length(f),1);
num = 0
for m = 1:length(f)
    %if mod(i,2) ~=0
        num = num + 1;
        predict_fun = dot(weight(1:19),f(m,1:19))+weight(20);
        result(m,:) = predict_fun;
end
end