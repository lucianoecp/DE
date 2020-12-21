clc;
clear all;


disp('RELATORIO:');

% Entrada de dados
[H,PD] = data4
%[P, CIC,CG] = de_sp(H,PD);


%disp('UNIDADE GERADORA/ GERAÇÃO OTIMA (MW)');
%P
%disp(' CUSTO DE COMBUSTÍVEL INCREMENTAL (Rs./MWhr)');
%CIC
%disp('CUSTO TOTAL DE GERAÇÃO(Rs./hr.)');
%CG

%PD = randi(1000,25,1)+550;

n = 25
PD = linspace(550,1500,n)

for i=1:n
    PD(i)
    [P, CIC,CG] = de_sp(H,PD(i));
    
    disp('UNIDADE GERADORA/ GERAÇÃO OTIMA (MW)');
    P
    disp(' CUSTO DE COMBUSTÍVEL INCREMENTAL (Rs./MWhr)');
    CIC
    disp('CUSTO TOTAL DE GERAÇÃO(Rs./hr.)');
    CG
    
    p(i,1)=P(2,1);
    p(i,2)=P(2,2);
    p(i,3)=P(2,3);
    
    lb(i)=CIC;
    ct(i) = CG;
    
end


y = p;
x = PD;

figure(1)
plot(x, y)
legend('P1','P2','P3')
title ('DEMANDA/GERACAO')
xlabel ('PD(i)')
ylabel ('P(i)')


y = lb;
x = ct;


figure(2)
plot(x, y)
title ('Custo incremental/custo total')
xlabel ('Custo total de Geração')
ylabel ('Lambda')



