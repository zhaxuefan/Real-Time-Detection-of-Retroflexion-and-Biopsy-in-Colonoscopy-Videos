function GA_LS
% ������С����ԭ�����Ŵ��㷨������ع�����
clear all;close all;clc
  

%-------------�Ŵ��㷨-----------------------------------------------------
% ʹ��gaoptimset�������в�������
options = gaoptimset('PopulationSize',400,'Generations',800,'PlotFcn',@gaplotbestf);
% PopulationSize - ��Ⱥ����
% Generations - �Ŵ��Ż�����
% PlotFcn - �������̻�ͼ


[k1,fva,reason,output,final_pop]=ga(@lineartarget,20,[],[],[],[],[],[],@ellipseparabola,options);
load('normalizedfeature.mat');
y = Profun(k1,f); % ProfunΪ�Զ���ķ��溯��
figure;plot(x,y,'b-',x,Profun(k1,x),'r--');
legend('ԭʼ����','�������');
fprintf('\n\n�Ŵ��㷨�ĳ�ʼ������ֵ:\n');
fprintf('\n\t���� a0 = %.9f',k1(1));
fprintf('\n\t���� b0 = %.9f',k1(2));
fprintf('\n\t���� c0 = %.9f',k1(3));
fprintf('\n\t���� d0 = %.9f',k1(4));
end
%-------------------------------------------------------------------------

%----------------�������Ŀ�꺯��-------------------------------------------
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

%-----------------�������ɺ���-----------------------------------------
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