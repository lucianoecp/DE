function [PU, ifc, totgencost] = de_sp(costdata,pd)

    
    ng=length(costdata(:,1));

    for i=1:ng
        uno(i)=costdata(i,1);
        a(i)=costdata(i,2);
        b(i)=costdata(i,3);
        d(i)=costdata(i,4);
        pmin(i)=costdata(i,5);
        pmax(i)=costdata(i,6);
    end

    lambda=9.0;
    delp=0.1;
    dellambda=0;

    for i=1:ng
        pv(i)=0;
        pvfin(i)=0;
    end

    while(abs(delp)>=0.0001)
        lambda=lambda+dellambda;
        sum=0;
        totgam=0;
        for i=1:ng
            p(i)=(lambda-b(i))/(2*d(i));
            sum=sum+p(i);
            totgam=totgam+0.5*(1/d(i));
        end
        delp=pd-sum;
        dellambda=delp/totgam;
        ifc=lambda;
    end

    limvio=0;

    for i=1:ng
        if(p(i)<pmin(i)|p(i)>pmax(i))
            limvio=1;
        break;
        end
    end

    if limvio==0
        disp('A GERAÇÃO ESTÁ DENTRO DOS LIMITES');
    end

    if (limvio==1)
        sum=0;
        totgam=0;
        delp=0.1;
        loprep=1;
        while(abs(delp)>=0.01&loprep==1)
            disp('A GERAÇÃO NÃO ESTÁ DENTRO DOS LIMITES');

            disp(strcat('GERADOR VIOLADO: G', num2str(i)));


            if p(i)<pmin(i)
                disp(strcat('GERAÇÃO EM (MW): ',num2str(p(i))));
                disp(strcat('O LIMITE MÍNIMO FOI VIOLADO, Pmin: ',...
                    num2str(pmin(i))));

            elseif p(i)>pmax(i)
                disp(strcat('GERAÇÃO EM (MW):',num2str(p(i))));
                disp(strcat('O LIMITE MÁXIMO FOI VIOLADO, Pmax: ',...
                    num2str(pmax(i))));
            end

            sum=0;
            totgam=0;

            for i=1:ng
                pv(i)=0;
            end
            for i=1:ng
                if (p(i)<pmin(i)|p(i)>pmax(i))
                if p(i)<pmin(i)
                    p(i)=pmin(i);
                else
                    p(i)=pmax(i);
                end
                pv(i)=1;
                pvfin(i)=1;
                break;
                end
            end
            for i=1:ng
                sum=sum+p(i);
                if (pvfin(i)~=1)
                    totgam=totgam+0.5*(1/d(i));
                end
            end
            delp=pd-sum;
            dellambda=delp/totgam;
            lambda=lambda+dellambda;
            ifc=lambda;

            for i=1:ng
                if pvfin(i)~=1
                    p(i)=(lambda-b(i))/(2*d(i));
                end
                sum=sum+p(i);
            end
            delp=pd-sum;
            loprep=0;
            for i=1:ng
                if p(i)<pmin(i)|p(i)>pmax(i)
                    loprep=1;
                    break;
                end
            end
        end
    end

    totgencost=0;

    for i=1:ng
        totgencost=totgencost+(a(i)+b(i)*p(i)+d(i)*p(i)*p(i));
    end
    disp(strcat('LAMBDA: ',num2str(lambda)))

    PU = [uno; p]

end