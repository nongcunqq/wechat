CREATE OR REPLACE PROCEDURE INVENTORY.sp_AnalysisAging_Arrange_20
(p_SAPClient IN VARCHAR2,p_DateFrom IN date,p_DateTo IN date,p_Re IN number,RES OUT VARCHAR2 )
AS
  v_CurrentDate VARCHAR2(20);
  v_ForDate date;
  v_Stock float;
  v_10Stock float;
  v_309Stock float;
  v_SAPCLIENT VARCHAR2(16) ;
  v_PLANT VARCHAR2(4) ;
  v_MATERIAL VARCHAR2(18); 
  v_PN VARCHAR2(18);  
  v_MBLNR VARCHAR2(30); 
  v_ZEILE VARCHAR2(10) ; 
  v_ENTRYDATE VARCHAR2(20); 
  v_REPORTDATE VARCHAR2(8); 
  v_TOTAL_STOCK FLOAT(126); 
  v_SUM_Stock FLOAT(126);
  v_TOTAL_VALUE FLOAT(126); 
  v_CURRENCY VARCHAR2(5); 
  v_BWART VARCHAR2(10); 
  v_invAging VARCHAR2(20 );
  v_Aging_PN VARCHAR2(18); 
  v_Aging_Stock FLOAT(126);
  v_Aging_Value FLOAT(126);
  v_AGING_DATE VARCHAR2(8); 
  v_Aging_Aging VARCHAR2(20 );
  v_j  number;

  E_ERROR EXCEPTION;
BEGIN
/*

   -- analysisflag is 0 是原數據狀態，只用 庫存量記錄； 1 是庫存量且將出入庫記錄導入； 4 已算完 309 庫存； 9 是分析且不再使用的單如 CASE3的記錄
set serveroutput on;
DECLARE RES varchar2(300);
BEGIN
RES:='OK';

sp_AnalysisAging_Arrange_20(to_date('2020-07-01' ,'yyyy-MM-dd')-360,to_date('2020-07-01' ,'yyyy-MM-dd') ,0,RES);
commit; 
END;

    update revenue.inv_configvalue set delflag='false',confignamedesc=to_char(p_DateTo,'yyyy-mm-dd') || ':' || p_SAPClient || '庫齡算中,預計執行時間（' || to_char(sysdate,'hh24:mi:ss')  || ' ~ ' ||to_char(sysdate+5/24,'hh24:mi:ss') ||'）, 請等待......刷新'
                where configname ='RevInvHomePage_notice'; commit;
 */
    RES:='1.begin SAPClient:' || p_SAPClient || ' DTF:' || p_DateFrom  || ' DTTo:' || p_DateTo || ' RE:' ||p_Re;
    INSERT INTO log_eventrecord (NAME, Msg) VALUES ('1_Begin','Inv_Aging_Arrange_New:'   || 'Runlog:'||RES);
    v_ForDate:= p_DateFrom;
    v_CurrentDate:=to_char(p_DateTo,'yyyymmdd');

    if p_Re!=0 then

         --INSERT INTO log_eventrecord (NAME, Msg) VALUES ('Re_Analysis','Inv_Aging_Recursive MBLNR:'  ||  'Runlog:'||RES);
          insert into inv_aging_arrange_history
            select 'AgingForMM',SAPCLIENT , PLANT , MATERIAL, MBLNR, ZEILE, ENTRYDATE, REPORTDATE , TOTAL_STOCK , SUM_STOCK , TOTAL_VALUE, CURRENCY , 
                    BWART , INVAGING, ANALYSISFLAG, AGING_STOCK , AGING_VALUE, AGING_DATE, AGING_AGING, AGING_PN , LASTEDITDT, LASTEDITBY, 
                    STORAGELC, REPORTDATE2, AGING_PLANT, p_Re
        from inv_aging_arrange where SAPCLIENT =p_SAPClient AND REPORTDATE2=v_CurrentDate;

        delete inv_aging_arrange where SAPCLIENT =p_SAPClient AND REPORTDATE2=v_CurrentDate;
        delete INV_AGING_DATE_LIST WHERE SAPCLIENT =p_SAPClient AND reportdate =v_CurrentDate;

    end if;

    v_SAPCLIENT:='';
    select nvl(b.sapclient,'') into v_SAPCLIENT  
        from (select 1 rn from dual) a  
        left join (  
        	SELECT sapclient,rownum rn FROM INV_AGING_DATE_LIST cc WHERE cc.SAPCLIENT =p_SAPClient AND cc.reportdate =v_CurrentDate and rownum <=1
        ) b on a.rn=b.rn  ;

    if length(v_SAPCLIENT) >0 then
        RES:=v_CurrentDate || ' 節點的庫齡記錄已存在，請先清除上次庫齡記錄后，再分析 庫齡';  
        RAISE E_ERROR; 
    else    

        EXECUTE   IMMEDIATE   'TRUNCATE   TABLE   Calendar_mm_wk_Aging';

        while p_DateTo >= v_ForDate loop
            insert into Calendar_mm_wk_Aging (Currentdate,CURRENTDATE2,CURRENTDATE3,curMonth,CUR_MONTH,CURMONTH_E,CURQuarter,CURWEEK_WW,CURWEEK_IW,CURWEEK_FM,CURWEEKDAY
                                ,InvQuarter,inv_MONTH,InvMONTH_E,invWEEK_IW,invyear,AGINGBATCH)
            select v_ForDate,to_char(v_ForDate,'yyyy-mm-dd'),to_char(v_ForDate,'yyyymmdd')
                    ,to_char(v_ForDate,'yyyymm'),to_char(v_ForDate,'yyyy-mm'),TO_CHAR(v_ForDate,'MON','NLS_DATE_LANGUAGE=AMERICAN'),trunc((to_char(v_ForDate,'mm')+2)/3)
                    ,to_char(v_ForDate,'ww'),to_char(v_ForDate,'iw'),to_char(v_ForDate,'FMWW'),to_char(v_ForDate,'day')
                    ,trunc((to_char(v_ForDate-1,'mm')+2)/3) as InvQuarter
                    ,to_char(v_ForDate-1,'yyyy-mm') as inv_MONTH
                    ,TO_CHAR(v_ForDate-1,'MON','NLS_DATE_LANGUAGE=AMERICAN') as InvMONTH_E
                    ,to_char(v_ForDate-1,'iw') as invWEEK_IW ,to_char(v_ForDate-1,'yyyy') as invyear,v_CurrentDate from dual;

            v_ForDate:= v_ForDate+1;        
        end loop;

        update Calendar_mm_wk_Aging set invAging = case when p_DateTo-Currentdate<31 then '0~30' 
            when p_DateTo-Currentdate>30 and p_DateTo-Currentdate<61 then '31~60'
            when p_DateTo-Currentdate>60 and p_DateTo-Currentdate<91 then '61~91'
            when p_DateTo-Currentdate>90 and p_DateTo-Currentdate<121 then '91~120'
            when p_DateTo-Currentdate>120 and p_DateTo-Currentdate<151 then '121~150'
            when p_DateTo-Currentdate>150 and p_DateTo-Currentdate<181 then '151~180'
            when p_DateTo-Currentdate>180 and p_DateTo-Currentdate<211 then '181~210'
            when p_DateTo-Currentdate>210 and p_DateTo-Currentdate<241 then '211~240'
            when p_DateTo-Currentdate>240 and p_DateTo-Currentdate<271 then '241~270'
            when p_DateTo-Currentdate>270 and p_DateTo-Currentdate<301 then '271~300'
            when p_DateTo-Currentdate>300 and p_DateTo-Currentdate<331 then '301~330'
            when p_DateTo-Currentdate>330 and p_DateTo-Currentdate<361 then '331~360'
            when p_DateTo-Currentdate>360  then '>360' end 
        where AGINGBATCH =v_CurrentDate ;

        EXECUTE   IMMEDIATE   'TRUNCATE   TABLE   inv_aging_arrange_tmp ';
        -- EXECUTE   IMMEDIATE   'TRUNCATE   TABLE   inv_aging_arrange';
        RES:='查找p_DateTo的所有倉庫存量';
        insert into  inv_aging_arrange_tmp  (SAPCLIENT,plant,material ,reportdate,reportdate2,TOTAL_STOCK,TOTAL_VALUE,CURRENCY,MBLNR,BWART,invAging,analysisflag)
        select a.SAPCLIENT,a.plant,a.material ,a.reportdate,a.reportdate,sum(a.TOTAL_STOCK),sum(a.TOTAL_VALUE),a.CURRENCY,'0000000000','999','>360',0
        from inv_inventory a
        where a.SAPCLIENT =p_SAPClient AND a.REPORTDATE=v_CurrentDate -- and a.plant in  ('GHUO','PIJ0','PIJ2','PIJ5','PIJ6','PIL6','IL8')
                   --and  a.plant in (  'SSSS','GHUO','SSSG','PIJ5')

                   --and  a.plant ='PIJ2' 
                   /*and a.material in ( 
                                     select distinct material from inv_aging_master
                                                                where bwart='309' and  mblnr in (select mblnr from inv_aging_master 
                                                                --where material in ('17J8W-LF','32040FV00-183-G'
                                                                 where material in ('M1077133-001','81080MH00-026-G','32040FV00-183-G','120110V00-232-G', '17J8W-LF','1A323WW00-G0001','1A32ERR00-600-G'
                                                               ))                                                        
                                        )*/
        group by   a.SAPCLIENT,a.plant,a.material ,a.reportdate, a.CURRENCY,'0000000000','999','>360',0  ;

        --INSERT INTO log_eventrecord (NAME, Msg) VALUES ('2_Begin','Inv_Aging_Recursive MBLNR:'  ||  'Runlog:'||RES);
        RES:='找出360天以內的出入庫記錄'; 
        insert into  inv_aging_arrange_tmp  (SAPCLIENT,plant,material ,MBLNR, ENTRYDATE,reportdate,reportdate2,TOTAL_STOCK,SUM_Stock,TOTAL_VALUE,CURRENCY,BWART,invAging,analysisflag)
                            select  a.SAPCLIENT,a.plant,a.material ,a.MBLNR, a.ENTRYDATE,b.currentdate3,v_CurrentDate,sum(a.quantityl),0,0,'NTD',a.BWART,b.invAging,0
                            from inv_aging_master a, Calendar_mm_wk_Aging b
                            where a.SAPCLIENT =p_SAPClient AND a.material is not null and a.postingdate<p_DateTo and b.currentdate2=a.postingdate and a.BWART in ('101','105','Z02','653','309')
                                    -- and  exists(select * from inv_aging_arrange_tmp  where sapclient=a.sapclient and plant=a.plant and material=a.material )
                            group by a.SAPCLIENT,a.plant,a.material ,a.MBLNR,a.ENTRYDATE,b.currentdate3,a.BWART,b.invAging,0,0,'NTD';
        --INSERT INTO log_eventrecord (NAME, Msg) VALUES ('3_Begin','Inv_Aging_Recursive MBLNR:'  ||  'Runlog:'||RES);
        commit; 

        RES:='計算庫齡 10. 先算 A料轉 B料， MVT=309, 由 B 料為';
        FOR item IN (
                    SELECT  SAPCLIENT,plant,material, MBLNR,ZEILE,ENTRYDATE,reportdate,TOTAL_STOCK,SUM_Stock,TOTAL_VALUE,CURRENCY,BWART,invAging,analysisflag
                    FROM inv_aging_arrange_tmp  
                    WHERE analysisflag=0 and BWART='309' and TOTAL_STOCK>0  and material in (select material from inv_inventory where SAPCLIENT=p_SAPClient) order by reportdate desc
                    ) loop 
                    RES:='';
                     v_Stock:=item.TOTAL_STOCK; v_309Stock:=0;  
                     v_SAPCLIENT:=item.SAPCLIENT; v_plant:=item.plant;  v_material:=item.material; v_REPORTDATE:=item.reportdate; v_TOTAL_STOCK:=item.TOTAL_STOCK;  v_TOTAL_VALUE :=item.TOTAL_VALUE;v_MBLNR:=item.MBLNR;
                    sp_AnalysisAging_Recursive(v_SAPCLIENT,v_plant,v_material, v_MBLNR,v_REPORTDATE,'309',v_TOTAL_STOCK,item.invAging,v_CurrentDate,0,RES);                   
         END loop ;
        RES:='將異動 庫存小于 0 的置無效單';
        update inv_aging_arrange_tmp   set  analysisflag =9,Aging_PN='無效單據'    WHERE   BWART ='309' and analysisflag= 0 and Aging_Stock<=0 ;   
        RES:='count 非 309 物料進行累減及取減數';
        /*  A料有效單據>= 庫存量的,使用累減方式算出 》0 的記錄时间计為A料库龄段*/
        v_j:=0;
        --execute immediate ' select count(1) from '||答tbl_name into a_num;
        SELECT COUNT(*) INTO  v_j  
        FROM (
                SELECT llwo.*  FROM (
                            select lrow.*, lag(lrow.dec_Stock,1) over (order by lrow.SAPCLIENT,lrow.PLANT,lrow.MATERIAL ,lrow.reportdate desc) as lagrow 
                            from (SELECT 
                                 t.SAPCLIENT,t.PLANT,t.MATERIAL ,t.MBLNR, t.REPORTDATE,t.TOTAL_STOCK,t.invAging,
                                 sum(DECODE(t.RN,1,t.TOTAL_STOCK,- t.TOTAL_STOCK)) OVER( PARTITION BY t.SAPCLIENT,t.PLANT,t.MATERIAL ORDER BY t.REPORTDATE desc,t.MBLNR) AS dec_Stock
                                FROM 
                                    (
                                    SELECT a.*,ROW_NUMBER() OVER(PARTITION BY a.SAPCLIENT, a.PLANT, a.MATERIAL     order BY  a.REPORTDATE desc,a.MBLNR) RN 
                                    FROM (                                        
                                         select t1.SAPCLIENT,t1.PLANT,t1.MATERIAL,t1.MBLNR,  t1.REPORTDATE,
                                                case when t1.Aging_Stock>0 then t1.Aging_Stock else t1.TOTAL_STOCK end TOTAL_STOCK,
                                                case when t1.Aging_Stock>0 then t1.aging_aging else t1.invAging end invAging                    
                                          FROM (select distinct ab.SAPCLIENT,ab.PLANT,ab.MATERIAL,ab.MBLNR, ab.REPORTDATE,ab.Aging_Stock,ab.TOTAL_STOCK,ab.invAging,ab.ANALYSISFLAG,ab.aging_aging from inv_aging_arrange_tmp  ab 
                                              WHERE   ab.ANALYSISFLAG=0 and ab.TOTAL_STOCK>0 -- and bwart!='999'
                                           --  WHERE   ab.ANALYSISFLAG=0  and ab.plant='GHUO' and ab.material='M1066327-002-L10'  
                                             ) t1 ) a
                                    )  t 
                             ) lrow-- where dec_Stock>=0 
                     ) llwo WHERE  llwo.lagrow>0 and rownum<2
            ) ;
        RES:='非 309 物料進行累減及取減數';             
        if v_j>0 then                                  
            MERGE INTO  inv_aging_arrange_tmp  z
                USING (
                        SELECT llwo.*  FROM (
                            select lrow.*, lag(lrow.dec_Stock,1) over (order by lrow.SAPCLIENT,lrow.PLANT,lrow.MATERIAL ,lrow.reportdate desc,lrow.MBLNR) as lagrow 
                            from (SELECT 
                                 t.SAPCLIENT,t.PLANT,t.MATERIAL ,t.MBLNR, t.REPORTDATE,t.TOTAL_STOCK,t.invAging,t.aging_date,
                                 sum(DECODE(t.RN,1,t.TOTAL_STOCK,- t.TOTAL_STOCK)) OVER( PARTITION BY t.SAPCLIENT,t.PLANT,t.MATERIAL ORDER BY t.REPORTDATE desc,t.MBLNR) AS dec_Stock
                                FROM 
                                    (
                                    SELECT a.*,ROW_NUMBER() OVER(PARTITION BY a.SAPCLIENT, a.PLANT, a.MATERIAL     order BY  a.REPORTDATE desc,a.MBLNR) RN 
                                    FROM (                                        
                                         select t1.SAPCLIENT,t1.PLANT,t1.MATERIAL,t1.MBLNR,  t1.REPORTDATE,
                                                case when t1.Aging_Stock>0 then t1.aging_date else t1.REPORTDATE end  aging_date,
                                                case when t1.Aging_Stock>0 then t1.Aging_Stock else t1.TOTAL_STOCK end TOTAL_STOCK,
                                                case when t1.Aging_Stock>0 then t1.aging_aging else t1.invAging end invAging                    
                                          FROM (select distinct ab.SAPCLIENT,ab.PLANT,ab.MATERIAL,ab.MBLNR, ab.REPORTDATE,aging_date,ab.Aging_Stock,ab.TOTAL_STOCK,ab.invAging,ab.ANALYSISFLAG,ab.aging_aging from inv_aging_arrange_tmp  ab 
                                              WHERE   ab.ANALYSISFLAG=0 and ab.TOTAL_STOCK>0 -- and bwart!='999'
                                           --  WHERE   ab.ANALYSISFLAG=0    and ab.material='M1066327-002-L10'  
                                             ) t1 ) a
                                    )  t 
                              ) lrow --where dec_Stock>=0 當Stock=17,有效單據分別是7+9+4 時此條件無效，如20200501 807	PIJ0	0101HTR00-000-G  4這筆的 Dec_stock=-3, Lagrow=1 
                     ) llwo WHERE  llwo.lagrow>0  --llwo.lagrow>=0 當Stock=3，有效單據分別是3+3 時此條件無效，如20200501807	PIJ0	1A42E1E00-600-GX04
                    ) t2 
                on (z.SAPCLIENT=t2.SAPCLIENT  AND  z.plant=t2.PLANT AND   z.material =t2.MATERIAL  and nvl(z.mblnr,' ')=nvl(t2.MBLNR,' ') AND z.REPORTDATE=t2.REPORTDATE and z.bwart!='999' )
                WHEN MATCHED THEN UPDATE SET z.aging_date = t2.aging_date, z.aging_aging=t2.invAging,z.ANALYSISFLAG=4   /*驗證 aging_stock已有值t2.TOTAL_STOCK*/
                                            ,z.aging_stock=CASE WHEN t2.dec_Stock> 0 THEN t2.TOTAL_STOCK ELSE t2.lagrow END,z.Aging_PN=t2.MATERIAL,z.sum_stock=t2.dec_Stock,z.lasteditby='A>lc11';
        end if;

        RES:='不足料扔 >360';
        v_j:=0;
        SELECT COUNT(*) INTO  v_j  
        FROM (
                select za.* from (
                                select ab.SAPCLIENT,ab.PLANT,ab.MATERIAL,ab.MBLNR, ab.REPORTDATE
                                         ,ab.ENTRYDATE
                                         ,ab.TOTAL_STOCK -nvl((select sum(aging_stock) from inv_aging_arrange_tmp  ag where ag.ANALYSISFLAG =4 and ag.SAPCLIENT=ab.SAPCLIENT  AND  ag.plant=ab.PLANT AND   ag.material =ab.MATERIAL  AND  ag.bwart!='999'),0) as TOTAL_STOCK
                                         ,TOTAL_VALUE,'>360' as invAging,4 as analysisflag
                                from inv_aging_arrange_tmp  ab where ab.ANALYSISFLAG=0 and ab.bwart='999' 

                            ) za
                where za.TOTAL_STOCK>0  and rownum<2
            );
        if v_j>0 then 
           MERGE INTO  inv_aging_arrange_tmp  z
                    USING (select za.* from (
                                            select ab.SAPCLIENT,ab.PLANT,ab.MATERIAL,ab.MBLNR, ab.REPORTDATE
                                                     ,ab.ENTRYDATE
                                                     ,ab.TOTAL_STOCK -nvl((select sum(aging_stock) from inv_aging_arrange_tmp  ag where ag.ANALYSISFLAG =4 and ag.SAPCLIENT=ab.SAPCLIENT  AND  ag.plant=ab.PLANT AND   ag.material =ab.MATERIAL  AND  ag.bwart!='999'),0) as TOTAL_STOCK
                                                     ,TOTAL_VALUE,'>360' as invAging,4 as analysisflag
                                            from inv_aging_arrange_tmp  ab where ab.ANALYSISFLAG=0 and ab.bwart='999' 

                                        ) za
                            where za.TOTAL_STOCK>0) t2
                    on (z.SAPCLIENT=t2.SAPCLIENT  AND  z.plant=t2.PLANT AND   z.material =t2.MATERIAL  and  z.bwart!='999' AND z.invAging ='>360')
                    WHEN NOT MATCHED THEN  INSERT  (z.SAPCLIENT, z.plant, z.material, z.CURRENCY,z.MBLNR, z.ZEILE,z.entrydate, z.reportdate,z.reportdate2, z.aging_date,z.TOTAL_STOCK, z.total_value,z.BWART, z.invAging,z.aging_stock,z.aging_aging,z.analysisflag,z.aging_pn,z.aging_plant,z.lasteditby)                                               
                                           VALUES  (t2.SAPCLIENT, t2.plant, t2.material ,'',     t2.MBLNR,'',     t2.entrydate,t2.reportdate,v_CurrentDate, '',         t2.TOTAL_STOCK,t2.total_value, '',    t2.invAging,t2.TOTAL_STOCK,t2.invAging, t2.analysisflag, t2.material,t2.plant,'Inv>LC' );

        end if;

        insert into inv_aging_arrange (SAPCLIENT,plant,material,MBLNR,ZEILE,ENTRYDATE,reportdate,reportdate2,TOTAL_STOCK,SUM_Stock,TOTAL_VALUE,CURRENCY,BWART,invAging,analysisflag,aging_stock ,aging_value,aging_date,  aging_aging , Aging_PN,lasteditdt,lasteditby,storagelc, aging_plant)
        select                                 SAPCLIENT,plant,material,MBLNR,ZEILE,ENTRYDATE,reportdate,reportdate2,TOTAL_STOCK,SUM_Stock,TOTAL_VALUE,CURRENCY,BWART,invAging,analysisflag,aging_stock ,aging_value,aging_date,  aging_aging , Aging_PN,lasteditdt,lasteditby,storagelc, aging_plant
        from inv_aging_arrange_tmp  where analysisflag =4; 

        RES:='OK';
    end if;

    --INSERT INTO log_eventrecord (NAME, Msg)  select 'Aging_End',('起始日' ||  p_DateFrom  || '截止日:'|| p_DateTo || 'RunBegin:' || v_CurrentDate ||'Runlog:'||RES) from dual;
    INSERT INTO INV_AGING_DATE_LIST (sapclient,reportdate) 
    SELECT p_SAPClient,v_CurrentDate FROM dual;

    update revenue.inv_configvalue set delflag='true'   where configname ='RevInvHomePage_notice'; 
commit;
EXCEPTION
    WHEN E_ERROR THEN 
        ROLLBACK; 
        INSERT INTO log_eventrecord (NAME, Msg) VALUES ('Aging_Error1','inv_aging_ar_tmp 起始日' || to_char(p_DateTo-360,'yyyymmdd') || '截止日:'|| p_DateTo ||  ' Plant:'|| v_plant  || ' PN:' || v_MATERIAL || ' v_MBLNR:'  || v_MBLNR || 'Runlog:'||RES);        
  /*  WHEN OTHERS THEN
        ROLLBACK;        
        INSERT INTO log_eventrecord (NAME, Msg) VALUES ('Aging_Err_o','inv_aging_ar_tmp 起始日' || to_char(p_DateTo-360,'yyyymmdd') || '截止日:'|| p_DateTo ||  'Plant:'|| v_plant  || 'PN:' || v_MATERIAL ||  ' v_MBLNR:'  || v_MBLNR ||  'Runlog:'||RES);  
        */
END;
