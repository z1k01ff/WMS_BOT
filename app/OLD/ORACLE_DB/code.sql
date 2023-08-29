CREATE OR REPLACE PACKAGE BODY TRP_TRANSPORT_FOR_USER IS

    HOW_MANY_TESTS CONSTANT NUMBER := 10;

    FUNCTION test_work_mode(p_wh_trans_id IN NUMBER
                           ,p_workmode    IN NUMBER) RETURN INTEGER AS

        v_sql          VARCHAR2(4000);
        v_work_mode_nr tma_work_mode.work_mode_nr%TYPE;
        v_res          INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_work_mode');

        SELECT work_mode_nr
        INTO   v_work_mode_nr
        FROM   tma_work_mode w
        WHERE  w.work_mode_id = p_workmode;

        v_sql := 'SELECT 1 FROM TMAV_TA_$WORKMODE$ WHERE OBJECT_ID = $WHTRANS$';
        v_sql := REPLACE(v_sql
                        ,'$WORKMODE$'
                        ,v_work_mode_nr);
        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);

        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_res;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_work_mode');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_work_mode');
            RETURN 1;
        END IF;
    END test_work_mode;

    FUNCTION test_whtrans_app(p_wh_trans_id IN NUMBER) RETURN INTEGER AS

        v_sql VARCHAR2(4000);
        v_res INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_whtrans_app');

        v_sql := 'SELECT 1 FROM TR_TRANSPORTS_FAST WHERE WH_TRANS_ID = $WHTRANS$ AND APP_NAME = ''QTR''';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_res;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_whtrans_app');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_whtrans_app');
            RETURN 1;
        END IF;
    END test_whtrans_app;

    FUNCTION test_whtrans_status(p_wh_trans_id IN NUMBER) RETURN INTEGER AS

        v_sql VARCHAR2(4000);
        v_res INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_whtrans_status');

        v_sql := 'SELECT 1 FROM TR_TRANSPORTS_FAST WHERE WH_TRANS_ID = $WHTRANS$ AND STATUS = ''AC''';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_res;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_whtrans_status');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_whtrans_status');
            RETURN 1;
        END IF;
    END test_whtrans_status;

    FUNCTION test_strict_user(p_wh_trans_id IN NUMBER
                             ,p_user_nr     IN VARCHAR2) RETURN INTEGER AS

        v_sql VARCHAR2(4000);
        v_res INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_strict_user');

        v_sql := 'SELECT 1 FROM TMA_TASK_FAST T WHERE T.OBJECT_ID = $WHTRANS$ ';
        v_sql := v_sql ||
                 ' AND (T.USER_STRICT IS  NULL OR T.USER_STRICT = ''$USER$'') ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);
        v_sql := REPLACE(v_sql
                        ,'$USER$'
                        ,p_user_nr);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_res;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_strict_user');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_strict_user');
            RETURN 1;
        END IF;
    END test_strict_user;

    FUNCTION test_strict_terminal(p_wh_trans_id IN NUMBER
                                 ,p_terminal    IN VARCHAR2) RETURN INTEGER AS

        v_sql VARCHAR2(4000);
        v_res INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_strict_terminal');

        v_sql := 'SELECT 1 FROM TMA_TASK_FAST T WHERE T.OBJECT_ID = $WHTRANS$ ';
        v_sql := v_sql ||
                 ' AND (T.TERMINAL_NR_STRICT IS  NULL OR T.TERMINAL_NR_STRICT = ''$TERM$'') ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);
        v_sql := REPLACE(v_sql
                        ,'$TERM$'
                        ,p_terminal);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_res;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_strict_terminal');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_strict_terminal');
            RETURN 1;
        END IF;
    END test_strict_terminal;

    FUNCTION test_routing_zone1(p_wh_trans_id IN NUMBER
                               ,p_vehicle     IN VARCHAR2) RETURN INTEGER AS

        v_sql             VARCHAR2(4000);
        v_zone_id         QWH_ROUTE_ZONES.ROUTE_ZONE_ID%TYPE;
        v_tr_mean_type_id QWH_TR_MEANS_TYPES.TRM_TYPE_ID%TYPE;
        v_is_pick         QWH_RZ_2_TM_ASSIGNMENT.IS_PICK%TYPE;
        v_min_level_nr    QWH_RZ_2_TM_ASSIGNMENT.MIN_LEVEL_NR%TYPE;
        v_max_level_nr    QWH_RZ_2_TM_ASSIGNMENT.MAX_LEVEL_NR%TYPE;
        v_level_nr        STORAGEPLACES.LEVEL_NR%TYPE;
        v_sp_id           STORAGEPLACES.SP_ID%TYPE;
        v_res             INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_routing_zone1');

        SELECT TRM_TYPE_ID
        INTO   v_tr_mean_type_id
        FROM   qwh_tr_means m
        WHERE  m.trmean_nr = p_vehicle;

        v_sql := 'SELECT ROUTE_ZONE_ID_START, SP_ID_START AS ROUTE_ZONE_ID FROM TMA_TASK_FAST ';
        v_sql := v_sql ||
                 ' WHERE OBJECT_ID = $WHTRANS$ AND TASK_TYPE_ID = 3  ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);

        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_zone_id, v_sp_id; -- tu mamy id strefy rutowania i miejsca, które nas interesuj¹
        END;

        -- na jakim poziomie jest miejsce pobrania?
        SELECT sp.level_nr
        INTO   v_level_nr
        FROM   storageplaces sp
        WHERE  sp.sp_id = v_sp_id;

        v_sql := 'SELECT is_pick, min_level_nr, max_level_nr, 1 FROM QWH_RZ_2_TM_ASSIGNMENT WHERE TRMEAN_TYPE_ID = $TYPE$ ';
        v_sql := v_sql || ' AND ROUTE_ZONE_ID = $ZONE$';
        v_sql := REPLACE(v_sql
                        ,'$TYPE$'
                        ,v_tr_mean_type_id);
        v_sql := REPLACE(v_sql
                        ,'$ZONE$'
                        ,v_zone_id);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_is_pick, v_min_level_nr, v_max_level_nr, v_res;
            IF v_is_pick = QSYS.PAR_NO THEN
                qcmp_trace.msg('Wózek nie ma w³¹czonego pobierania w strefie startowej');
                v_res := NULL;
            END IF;

            IF v_level_nr < v_min_level_nr THEN
                qcmp_trace.msg('Miejsce jest zbyt nisko w stefie startowej');
                v_res := NULL;
            END IF;
            IF v_level_nr > v_max_level_nr THEN
                qcmp_trace.msg('Miejsce jest zbyt wysoko w stefie startowej');
                v_res := NULL;
            END IF;
        EXCEPTION
            WHEN no_data_found THEN
                qcmp_trace.msg('Brak przypisania wózka do stefy startowej');
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_routing_zone1');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_routing_zone1');
            RETURN 1;
        END IF;
    END test_routing_zone1;

    FUNCTION test_routing_zone2(p_wh_trans_id IN NUMBER
                               ,p_vehicle     IN VARCHAR2) RETURN INTEGER AS

        v_sql             VARCHAR2(4000);
        v_zone_id         QWH_ROUTE_ZONES.ROUTE_ZONE_ID%TYPE;
        v_tr_mean_type_id QWH_TR_MEANS_TYPES.TRM_TYPE_ID%TYPE;
        v_is_put          QWH_RZ_2_TM_ASSIGNMENT.IS_PUT%TYPE;
        v_min_level_nr    QWH_RZ_2_TM_ASSIGNMENT.MIN_LEVEL_NR%TYPE;
        v_max_level_nr    QWH_RZ_2_TM_ASSIGNMENT.MAX_LEVEL_NR%TYPE;
        v_level_nr        STORAGEPLACES.LEVEL_NR%TYPE;
        v_sp_id           STORAGEPLACES.SP_ID%TYPE;
        v_res             INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_routing_zone2');

        SELECT TRM_TYPE_ID
        INTO   v_tr_mean_type_id
        FROM   qwh_tr_means m
        WHERE  m.trmean_nr = p_vehicle;

        v_sql := 'SELECT ROUTE_ZONE_ID_FINISH, SP_ID_FINISH FROM TMA_TASK_FAST ';
        v_sql := v_sql ||
                 ' WHERE OBJECT_ID = $WHTRANS$ AND TASK_TYPE_ID = 3  ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);

        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_zone_id, v_sp_id; -- tu mamy id strefy rutowania i miejsca, które nas interesuj¹
        END;

        -- na jakim poziomie jest miejsce odk³adania?
        SELECT sp.level_nr
        INTO   v_level_nr
        FROM   storageplaces sp
        WHERE  sp.sp_id = v_sp_id;

        v_sql := 'SELECT is_put, min_level_nr, max_level_nr, 1 FROM QWH_RZ_2_TM_ASSIGNMENT WHERE TRMEAN_TYPE_ID = $TYPE$ ';
        v_sql := v_sql || ' AND ROUTE_ZONE_ID = $ZONE$';
        v_sql := REPLACE(v_sql
                        ,'$TYPE$'
                        ,v_tr_mean_type_id);
        v_sql := REPLACE(v_sql
                        ,'$ZONE$'
                        ,v_zone_id);

        qcmp_trace.msg(v_sql);
        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_is_put, v_min_level_nr, v_max_level_nr, v_res;
            IF v_is_put = QSYS.PAR_NO THEN
                qcmp_trace.msg('Wózek nie ma w³¹czonego odk³adania w strefie koñcowej');
                v_res := NULL;
            END IF;

            IF v_level_nr < v_min_level_nr THEN
                qcmp_trace.msg('Miejsce jest zbyt wysoko w stefie koñcowej');
                v_res := NULL;
            END IF;
            IF v_level_nr > v_max_level_nr THEN
                qcmp_trace.msg('Miejsce jest zbyt wysoko w stefie koñcowej');
                v_res := NULL;
            END IF;
        EXCEPTION
            WHEN no_data_found THEN
                qcmp_trace.msg('Brak przypisania wózka do stefy koñcowej');
        END;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_routing_zone2');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_routing_zone2');
            RETURN 1;
        END IF;
    END test_routing_zone2;

    FUNCTION test_vehicle_max_reach_level(p_wh_trans_id IN NUMBER
                                         ,p_vehicle     IN VARCHAR2)
        RETURN INTEGER AS

        v_sql          VARCHAR2(4000);
        v_min_level_nr NUMBER;
        v_max_level_nr NUMBER;
        v_level_nr1    STORAGEPLACES.LEVEL_NR%TYPE;
        v_level_nr2    STORAGEPLACES.LEVEL_NR%TYPE;
        v_sp_id1       STORAGEPLACES.SP_ID%TYPE;
        v_sp_id2       STORAGEPLACES.SP_ID%TYPE;
        v_res          INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_vehicle_max_reach_level');

        SELECT tr_mt.MIN_LEVEL_NR
              ,tr_mt.MAX_LEVEL_NR
        INTO   v_min_level_nr
              ,v_max_level_nr
        FROM   QWH_TR_MEANS_TYPES tr_mt
              ,QWH_TR_MEANS       tr_m
        WHERE  tr_mt.TRM_TYPE_ID = tr_m.TRM_TYPE_ID
        AND    tr_m.TRMEAN_NR = p_vehicle;

        qcmp_trace.msg('Minimalny poziom dla œr. transp. ' ||
                       v_min_level_nr);
        qcmp_trace.msg('Maksymalny poziom dla œr. transp. ' ||
                       v_max_level_nr);

        v_sql := 'SELECT SP_ID_START, SP_ID_FINISH AS ROUTE_ZONE_ID FROM TMA_TASK_FAST ';
        v_sql := v_sql ||
                 ' WHERE OBJECT_ID = $WHTRANS$ AND TASK_TYPE_ID = 3  ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);

        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_sp_id1, v_sp_id2; -- tu mamy miejsca, które nas interesuj¹
        END;

        -- na jakim poziomie jest miejsce pobierania?
        SELECT sp.level_nr
        INTO   v_level_nr1
        FROM   storageplaces sp
        WHERE  sp.sp_id = v_sp_id1;
        qcmp_trace.msg('Miejsce w stefie startowej poziom ' || v_level_nr1);

        -- na jakim poziomie jest miejsce odk³adania?
        SELECT sp.level_nr
        INTO   v_level_nr2
        FROM   storageplaces sp
        WHERE  sp.sp_id = v_sp_id2;
        qcmp_trace.msg('Miejsce w stefie koñcowej poziom ' || v_level_nr2);

        v_res := 1;

        IF v_level_nr1 < v_min_level_nr THEN
            qcmp_trace.msg('Miejsce jest zbyt nisko w stefie startowej');
            v_res := NULL;
        END IF;
        IF v_level_nr1 > v_max_level_nr THEN
            qcmp_trace.msg('Miejsce jest zbyt wysoko w stefie startowej');
            v_res := NULL;
        END IF;

        IF v_level_nr2 < v_min_level_nr THEN
            qcmp_trace.msg('Miejsce jest zbyt nisko w stefie koñcowej');
            v_res := NULL;
        END IF;
        IF v_level_nr2 > v_max_level_nr THEN
            qcmp_trace.msg('Miejsce jest zbyt wysoko w stefie koñcowej');
            v_res := NULL;
        END IF;

        IF v_res IS NULL THEN
            qcmp_trace.msg(v_sql);
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_vehicle_max_reach_level');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_vehicle_max_reach_level');
            RETURN 1;
        END IF;
    END test_vehicle_max_reach_level;

    FUNCTION test_count_vehicle_in_zones(p_wh_trans_id IN NUMBER
                                        ,p_vehicle     IN VARCHAR2)
        RETURN INTEGER AS

        v_sql        VARCHAR2(4000);
        v_zone1      QWH_ROUTE_ZONES.ROUTE_ZONE_ID%TYPE;
        v_zone2      QWH_ROUTE_ZONES.ROUTE_ZONE_ID%TYPE;
        v_tr_mean_id QWH_TR_MEANS.TRMEAN_ID%TYPE;
        v_res        INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_count_vehicle_in_zones');

        SELECT TR_M.TRM_TYPE_ID
        INTO   v_tr_mean_id
        FROM   QWH_TR_MEANS TR_M
        WHERE  TR_M.TRMEAN_NR = p_vehicle;

        v_sql := 'SELECT ROUTE_ZONE_ID_START, ROUTE_ZONE_ID_FINISH AS ROUTE_ZONE_ID FROM TMA_TASK_FAST ';
        v_sql := v_sql ||
                 ' WHERE OBJECT_ID = $WHTRANS$ AND TASK_TYPE_ID = 3  ';

        v_sql := REPLACE(v_sql
                        ,'$WHTRANS$'
                        ,p_wh_trans_id);

        BEGIN
            EXECUTE IMMEDIATE v_sql
                INTO v_zone1, v_zone2; -- tu mamy strefy, które nas interesuj¹
        END;

        v_res := 1;
        -- sprawdzamy zajêtoœæ w strefie1
        SELECT qwhp_trmn_rz_occup.AllowTrmInRZCount(v_tr_mean_id
                                                   ,v_zone1)
        INTO   v_res
        FROM   dual;

        IF v_res <> 1 THEN
            qcmp_trace.msg('Przekroczona iloœæ wózków w strefie startowej');
            v_res := NULL;
        END IF;

        -- sprawdzamy zajêtoœæ w strefie2
        SELECT qwhp_trmn_rz_occup.AllowTrmInRZCount(v_tr_mean_id
                                                   ,v_zone2)
        INTO   v_res
        FROM   dual;

        IF v_res <> 1 THEN
            qcmp_trace.msg('Przekroczona iloœæ wózków w strefie koñcowej');
            v_res := NULL;
        END IF;

        IF v_res IS NULL THEN
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_count_vehicle_in_zones');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_count_vehicle_in_zones');
            RETURN 1;
        END IF;
    END test_count_vehicle_in_zones;

    FUNCTION test_picking_zones(p_wh_trans_id IN NUMBER
                               ,p_workmode_id IN NUMBER) RETURN INTEGER AS
        -- tylko dla ZZT
        v_sql                 VARCHAR2(4000);
        v_use_pick_zones_mode BOOLEAN;
        v_res                 INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.test_picking_zones');

        v_use_pick_zones_mode := (qsys.GetParam2('NRF_USE_MODE_PICK_ZONE_IN_TRO_WAIT') =
                                 QSYS.PAR_YES);

        IF NOT v_use_pick_zones_mode THEN
            qcmp_trace.msg('Parametr NRF_USE_MODE_PICK_ZONE_IN_TRO_WAIT nie jest w³¹czony');
            v_res := NULL;
        ELSE
            -- w tym wypadku jeœli znajdziemy jakiœ rekord to niedobrze
            -- sprawdzane s¹ tylko miejsca Ÿród³owe ZZT
            v_sql := '
            SELECT 1 FROM TR_TRANSPORT_ITEMS_FAST tri
            WHERE  tri.WH_TRANS_ID = $WHTRANS$
            AND NOT EXISTS
            (SELECT 1 FROM QWH_PICK_ZONES_ASSIGN pza,
             (SELECT pz.pzone_id FROM qwh_pick_zones pz
             ,(SELECT t.work_mode_id, t.object_id,t.object_type FROM
                      QCM_ENVIRONMENT_WORK_MODE t
                      WHERE t.work_mode_id = $WH_MODE_ID)   mu
             WHERE  mu.object_type = ''PZ''
             AND   decode(mu.object_id,pz.pzone_id,-1,-1,-1,0)=-1)  my_pz
             WHERE pza.PZONE_ID = my_pz.PZONE_ID AND pza.SP_ID = tri.LU_SRC_SP_ID)
             AND EXISTS
             (SELECT 1 FROM QWH_PICK_ZONES_ASSIGN pza
             WHERE pza.SP_ID = tri.LU_SRC_SP_ID)';

            v_sql := REPLACE(v_sql
                            ,'$WHTRANS$'
                            ,p_wh_trans_id);
            v_sql := REPLACE(v_sql
                            ,'$WH_MODE_ID'
                            ,p_workmode_id);
            qcmp_trace.msgSQL(v_sql);

            BEGIN
                EXECUTE IMMEDIATE v_sql
                    INTO v_res;
            EXCEPTION
                WHEN no_data_found THEN
                    NULL;
            END;

        END IF;
        IF v_res IS NOT NULL THEN

            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_picking_zones');
            RETURN 0;
        ELSE
            qcmp_trace.return('TRP_TRANSPORT_FOR_USER.test_picking_zones');
            RETURN 1;
        END IF;
    END test_picking_zones;

    PROCEDURE init_test_result IS
        v_ctrl VARCHAR2(40);
    BEGIN
        FOR i IN 1 .. HOW_MANY_TESTS LOOP
            v_ctrl := 'LO_PIC' || to_char(i);
            qsyp_attrib_values.SetAttrib(v_ctrl
                                        ,'PICTURE'
                                        ,'wms_question_16.png');
        END LOOP;
    END init_test_result;

    PROCEDURE INIT_DATA(p_work_mode     IN OUT NUMBER
                       ,p_rec_where     IN OUT VARCHAR2
                       ,p_selected_rows IN OUT VARCHAR2
                       ,p_call_form     IN OUT VARCHAR2
                       ,p_call_control  IN OUT VARCHAR2) IS

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.INIT_DATA');

        init_test_result;

        qsyp_attrib_values.SetAttrib('BTN_TRMTYPE'
                                    ,'IS_DISPLAYED'
                                    ,'N');

        qsyp_attrib_values.SetAttrib('BTN_ZONE1'
                                    ,'IS_DISPLAYED'
                                    ,'N');

        qsyp_attrib_values.SetAttrib('BTN_ZONE2'
                                    ,'IS_DISPLAYED'
                                    ,'N');

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.INIT_DATA');
    END INIT_DATA;

    /******************************************************************************/
    /* Name : CHILD_CLOSED
    /* Author   : Pawe³ Stêpniowski
    /* Date : 2016.08.05
    /*----------------------------------------------------------------------------*/
    /* Purpose :
    /*----------------------------------------------------------------------------*/
    /* Parameter (I) :
    /*----------------------------------------------------------------------------*/
    /* Parameter (O) :
    /*----------------------------------------------------------------------------*/
    /* Exceptions :
    /******************************************************************************/
    PROCEDURE CHILD_CLOSED(p_terminal_nr   IN OUT VARCHAR2
                          ,p_user_nr       IN OUT VARCHAR2
                          ,p_trans_mean_nr IN OUT VARCHAR2
                          ,p_work_mode_id  IN OUT NUMBER
                          ,p_work_mode     IN OUT NUMBER
                          ,p_rec_where     IN OUT VARCHAR2
                          ,p_selected_rows IN OUT VARCHAR2
                          ,p_call_form     IN OUT VARCHAR2
                          ,p_call_control  IN OUT VARCHAR2
                          ,p_child_where   IN OUT VARCHAR2) AS
        -- tu to co wybrano ze spreada szukaj¹cego !!!

        v_SQL CLOB;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.CHILD_CLOSED');
        qcmp_trace.param('p_work_mode'
                        ,p_work_mode);
        qcmp_trace.param('p_rec_where'
                        ,p_rec_where);
        qcmp_trace.param('p_selected_rows'
                        ,p_selected_rows);
        qcmp_trace.param('p_call_form'
                        ,p_call_form);
        qcmp_trace.param('p_call_control'
                        ,p_call_control);
        qcmp_trace.param('p_child_where'
                        ,p_child_where);

        IF p_call_form = 'QWH_TR_TERMINAL_STATES' THEN

            IF p_child_where IS NOT NULL THEN
                v_SQL := 'SELECT SE.TERMINAL_NAME
                            ,SU.USER_NR
                            ,tm.TRMEAN_NR
                            ,se.WORK_MODE_ID
                      FROM   QWH_TR_MEANS tm
                            ,QTR_SESSIONS se
                            ,QCM_SYSUSERS su
                      WHERE  ' ||
                         REPLACE(p_child_where
                                ,'TERMINAL_NAME'
                                ,'tm.TRMEAN_NR') ||
                         '  AND    tm.TRMEAN_NR = se.TMEAN_NR
                        AND    su.USER_ID = se.LM_USER';

                EXECUTE IMMEDIATE v_SQL
                    INTO p_terminal_nr, p_user_nr, p_trans_mean_nr, p_work_mode_id;
            END IF;

        END IF;

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.CHILD_CLOSED');
    END CHILD_CLOSED;

    PROCEDURE TO_CHANGE(p_wh_trans_nr IN VARCHAR2) IS
        v_is_complex tr_transports_fast.is_complex%TYPE;
        v_pos_count  INTEGER;
        v_operation  VARCHAR2(255);
        v_oper_nr    tr_transports_fast.object_nr%TYPE;
        v_sp1        storageplaces.sp_nr%TYPE;
        v_sp2        storageplaces.sp_nr%TYPE;
        v_zone1      qwh_route_zones.route_zone_nr%TYPE;
        v_zone2      qwh_route_zones.route_zone_nr%TYPE;
        v_status     VARCHAR2(255);

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.TO_CHANGE');
        qcmp_trace.param('p_wh_trans_nr'
                        ,p_wh_trans_nr);

        init_test_result;

        qsyp_attrib_values.SetAttrib('LO_TR_INFO'
                                    ,'IS_DISPLAYED'
                                    ,'T');

        qsyp_attrib_values.SetAttrib('BTN_ZONE1'
                                    ,'IS_DISPLAYED'
                                    ,'T');

        qsyp_attrib_values.SetAttrib('BTN_ZONE2'
                                    ,'IS_DISPLAYED'
                                    ,'T');

        BEGIN
            SELECT t.is_complex
                  ,sc1.class_name
                  ,t.object_nr
                  ,sp1.sp_nr
                  ,sp2.sp_nr
                  ,rz1.route_zone_nr
                  ,rz2.route_zone_nr
                  ,sc2.class_name
            INTO   v_is_complex
                  ,v_operation
                  ,v_oper_nr
                  ,v_sp1
                  ,v_sp2
                  ,v_zone1
                  ,v_zone2
                  ,v_status
            FROM   tr_transports_fast t
                  ,qcm_sysclasses     sc1
                  ,qcm_sysclasses     sc2
                  ,storageplaces      sp1
                  ,storageplaces      sp2
                  ,qwh_route_zones    rz1
                  ,qwh_route_zones    rz2
            WHERE  t.wh_trans_id = to_number(p_wh_trans_nr)
            AND    sc1.class_type = 'TRANSPORT_OPER_TYPE'
            AND    sc1.class_value = t.transport_type_nr
            AND    sc2.class_type = 'WH_TRANSPORTS_STATUS'
            AND    sc2.class_value = t.status
            AND    sp1.sp_id = t.sp_id_start
            AND    sp2.sp_id = t.sp_id_finish
            AND    rz1.route_zone_id = sp1.route_zone_id
            AND    rz2.route_zone_id = sp2.route_zone_id;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;

        IF v_is_complex = qsys.par_yes THEN
            qsyp_attrib_values.SetAttrib('LBL_TO_SIMPLE_VAL'
                                        ,'VALUE'
                                        ,qcmp_nls.GETSTRING('TXT_TO_COMPLEX'));
            -- test 10 to test wy³¹cznie dla zleceñ z³o¿onych
            qsyp_attrib_values.SetAttrib('LO_TEST_10'
                                        ,'IS_DISPLAYED'
                                        ,'T');
            SELECT COUNT(*)
            INTO   v_pos_count
            FROM   tr_transport_items_fast ti
            WHERE  ti.wh_trans_id = to_number(p_wh_trans_nr);

        ELSIF v_is_complex = qsys.par_no THEN
            qsyp_attrib_values.SetAttrib('LBL_TO_SIMPLE_VAL'
                                        ,'VALUE'
                                        ,qcmp_nls.GETSTRING('TXT_TO_NORMAL'));

            qsyp_attrib_values.SetAttrib('LO_TEST_10'
                                        ,'IS_DISPLAYED'
                                        ,'N');

            v_pos_count := 1;
        ELSE
            qsyp_attrib_values.SetAttrib('LBL_TO_SIMPLE_VAL'
                                        ,'VALUE'
                                        ,'');

        END IF;

        qsyp_attrib_values.SetAttrib('LBL_POS_COUNT_VAL'
                                    ,'VALUE'
                                    ,v_pos_count);

        IF v_oper_nr IS NOT NULL THEN
            v_operation := v_operation || ' ' || v_oper_nr;
        END IF;

        qsyp_attrib_values.SetAttrib('LBL_TO_OPER_VAL'
                                    ,'VALUE'
                                    ,v_operation);

        qsyp_attrib_values.SetAttrib('LBL_LOCATION_FROM_VAL'
                                    ,'VALUE'
                                    ,v_sp1);

        qsyp_attrib_values.SetAttrib('LBL_LOCATION_TO_VAL'
                                    ,'VALUE'
                                    ,v_sp2);

        qsyp_attrib_values.SetAttrib('LBL_START_ZONE_VAL'
                                    ,'VALUE'
                                    ,v_zone1);

        qsyp_attrib_values.SetAttrib('LBL_FINISH_ZONE_VAL'
                                    ,'VALUE'
                                    ,v_zone2);

        qsyp_attrib_values.SetAttrib('LBL_STATUS_VAL'
                                    ,'VALUE'
                                    ,v_status);

        qsys_frm.stop_refresh('TR_TRANSPORT_FOR_USER_TEST_FD');

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.TO_CHANGE');
    END TO_CHANGE;

    PROCEDURE USER_CHANGE(p_user_nr IN VARCHAR2) IS

        v_user_group qcm_sysgroups.name%TYPE;

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.USER_CHANGE');
        qcmp_trace.param('p_user_nr'
                        ,p_user_nr);

        init_test_result;

        SELECT g.name
        INTO   v_user_group
        FROM   qcm_sysgroups g
              ,qcm_sysusers  u
        WHERE  u.group_id = g.group_id
        AND    u.user_nr = p_user_nr;

        qsyp_attrib_values.SetAttrib('LBL_UGROUP_VAL'
                                    ,'VALUE'
                                    ,v_user_group);

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.USER_CHANGE');
    END USER_CHANGE;

    PROCEDURE VEHICLE_CHANGE(p_vehicle_nr IN VARCHAR2) IS

        v_trm_type qwh_tr_means_types.name%TYPE;

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.VEHICLE_CHANGE');
        qcmp_trace.param('p_vehicle_nr'
                        ,p_vehicle_nr);

        init_test_result;

        SELECT t.name
        INTO   v_trm_type
        FROM   qwh_tr_means_types t
              ,qwh_tr_means       v
        WHERE  v.trm_type_id = t.trm_type_id
        AND    v.trmean_nr = p_vehicle_nr;

        qsyp_attrib_values.SetAttrib('LBL_TRMTYPE_VAL'
                                    ,'VALUE'
                                    ,v_trm_type);
        qsyp_attrib_values.SetAttrib('BTN_TRMTYPE'
                                    ,'IS_DISPLAYED'
                                    ,'T');

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.VEHICLE_CHANGE');
    END VEHICLE_CHANGE;

    PROCEDURE WORKMODE_CHANGE IS

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.WORKMODE_CHANGE');

        init_test_result;

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.WORKMODE_CHANGE');
    END WORKMODE_CHANGE;

    PROCEDURE TERMINAL_CHANGE IS

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.TERMINAL_CHANGE');

        init_test_result;

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.TERMINAL_CHANGE');
    END TERMINAL_CHANGE;

    PROCEDURE TEST_TO(p_wh_trans_id IN VARCHAR2
                     ,p_terminal    IN VARCHAR2
                     ,p_user        IN VARCHAR2
                     ,p_vehicle     IN VARCHAR2
                     ,p_workmode_id IN NUMBER) IS
        v_ctrl       VARCHAR2(40);
        v_is_complex tr_transports_fast.is_complex%TYPE;
        v_dummy      INTEGER;
        v_result     INTEGER;
    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.TEST_TO');
        qcmp_trace.param('p_wh_trans_id'
                        ,p_wh_trans_id);
        qcmp_trace.param('p_terminal'
                        ,p_terminal);
        qcmp_trace.param('p_user'
                        ,p_user);
        qcmp_trace.param('p_vehicle'
                        ,p_vehicle);
        qcmp_trace.param('p_workmode_id'
                        ,p_workmode_id);

        IF p_wh_trans_id IS NULL OR p_terminal IS NULL OR p_user IS NULL OR
           p_vehicle IS NULL OR p_workmode_id IS NULL THEN
            qcmp_error.qraise('TXT_REQUIRED_FIELDS_EMPTY');
        END IF;

        -- czy w tym trybie pracy s¹ zlecenia transportowe?
        BEGIN
            SELECT 1
            INTO   v_dummy
            FROM   tma_wm_task_type
            WHERE  task_type_id = 3
            AND    work_mode_id = p_workmode_id;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;
        IF v_dummy IS NULL THEN
            qcmp_error.qraise('TXT_TO_NOT_ASSIGNED_WORKMODE');
        END IF;
        v_dummy := NULL;

        -- sprawdzamy przypisanie grupy uzytkowników do trybu pracy
        BEGIN
            SELECT 1
            INTO   v_dummy
            FROM   tma_wm_ugroup t
                  ,qcm_sysusers  u
            WHERE  u.group_id = t.group_id
            AND    u.user_nr = p_user
            AND    t.work_mode_id = p_workmode_id;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;
        IF v_dummy IS NULL THEN
            qcmp_error.qraise('TXT_GR_NOT_ASSIGNED_WORKMODE');
        END IF;
        v_dummy := NULL;

        -- sprawdzamy przypisanie typu wózka do trybu pracy
        BEGIN
            SELECT 1
            INTO   v_dummy
            FROM   tma_wm_tr_mean_type t
                  ,qwh_tr_means_types  tt
                  ,qwh_tr_means        tm
            WHERE  t.work_mode_id = p_workmode_id
            AND    t.tr_mean_type_id = tt.trm_type_id
            AND    tt.trm_type_id = tm.trm_type_id
            AND    tm.trmean_nr = p_vehicle;
        EXCEPTION
            WHEN no_data_found THEN
                NULL;
        END;
        IF v_dummy IS NULL THEN
            qcmp_error.qraise('TXT_TRM_NOT_ASSIGNED_WORKMODE');
        END IF;

        -- wy³¹czamy teksty z testami
        FOR i IN 1 .. HOW_MANY_TESTS LOOP
            v_ctrl := 'LO_TEST_' || to_char(i);
            qsyp_attrib_values.SetAttrib(v_ctrl
                                        ,'IS_DISPLAYED'
                                        ,'N');
        END LOOP;

        SELECT t.is_complex
        INTO   v_is_complex
        FROM   tr_transports_fast t
        WHERE  t.wh_trans_id = p_wh_trans_id;

        v_result := 1;
        FOR i IN 1 .. HOW_MANY_TESTS LOOP
            IF v_result = 0 THEN
                EXIT;
            END IF;

            v_ctrl := 'LO_TEST_' || to_char(i);
            qsyp_attrib_values.SetAttrib(v_ctrl
                                        ,'IS_DISPLAYED'
                                        ,'T');
            v_ctrl := 'LO_PIC' || to_char(i);

            IF i = 1 THEN
                v_result := test_work_mode(p_wh_trans_id
                                          ,p_workmode_id);
            ELSIF i = 2 THEN
                v_result := test_whtrans_app(p_wh_trans_id);
            ELSIF i = 3 THEN
                v_result := test_whtrans_status(p_wh_trans_id);
            ELSIF i = 4 THEN
                v_result := test_strict_user(p_wh_trans_id
                                            ,p_user);
            ELSIF i = 5 THEN
                v_result := test_strict_terminal(p_wh_trans_id
                                                ,p_terminal);
            ELSIF i = 6 THEN
                v_result := test_routing_zone1(p_wh_trans_id
                                              ,p_vehicle);
            ELSIF i = 7 THEN
                v_result := test_routing_zone2(p_wh_trans_id
                                              ,p_vehicle);
            ELSIF i = 8 THEN
                v_result := test_vehicle_max_reach_level(p_wh_trans_id
                                                        ,p_vehicle);
            ELSIF i = 9 THEN

                v_result := test_count_vehicle_in_zones(p_wh_trans_id
                                                       ,p_vehicle);

            ELSIF i = 10 THEN
                IF v_is_complex = qsys.PAR_YES THEN
                    v_result := test_picking_zones(p_wh_trans_id
                                                  ,p_workmode_id);
                ELSE
                    qsyp_attrib_values.SetAttrib('LO_TEST_' || to_char(i)
                                                ,'IS_DISPLAYED'
                                                ,'N');
                    v_result := 1;
                END IF;
            END IF;

            IF v_result = 0 THEN

                qsyp_attrib_values.SetAttrib(v_ctrl
                                            ,'PICTURE'
                                            ,'wms_err_16.png');
            ELSE
                qsyp_attrib_values.SetAttrib(v_ctrl
                                            ,'PICTURE'
                                            ,'wms_ok_16.png');
            END IF;
            qsys_frm.stop_refresh('TR_TRANSPORT_FOR_USER_TEST_FD');
        END LOOP;

        qcmp_trace.return('TRP_TRANSPORT_FOR_USER.TEST_TO');
    END TEST_TO;

    PROCEDURE SHOW_VEHICLE_TYPE(p_vehicle_type IN VARCHAR2) IS

        v_trm_type_id qwh_tr_means_types.trm_type_id%TYPE;

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.SHOW_VEHICLE_TYPE');
        qcmp_trace.param('p_vehicle_type'
                        ,p_vehicle_type);

        SELECT t.trm_type_id
        INTO   v_trm_type_id
        FROM   qwh_tr_means_types t
        WHERE  t.trm_type_nr = p_vehicle_type;

        qsyp_actions.addaction('Q_ACTION_OPEN_FORM');
        qsyp_actions.addparam('FORMNAME'
                             ,'QWH_WH_TRMEANS_TYPES_FD');
        qsyp_actions.addparam('WORKMODE'
                             ,'EDIT');
        qsyp_actions.addparam('WHERE'
                             ,'TRM_TYPE_ID=' || v_trm_type_id);

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.SHOW_VEHICLE_TYPE');
    END SHOW_VEHICLE_TYPE;

    PROCEDURE SHOW_WORKMODE(p_workmode_id IN NUMBER) IS

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.SHOW_WORKMODE');
        qcmp_trace.param('p_workmode_id'
                        ,p_workmode_id);

        /*SELECT t.trm_type_id
        INTO   v_trm_type_id
        FROM   qwh_tr_means_types t
        WHERE  t.trm_type_nr = p_vehicle_type;*/

        qsyp_actions.addaction('Q_ACTION_OPEN_FORM');
        qsyp_actions.addparam('FORMNAME'
                             ,'TMA_WORK_MODES_FD');
        qsyp_actions.addparam('WORKMODE'
                             ,'EDIT');
        qsyp_actions.addparam('WHERE'
                             ,'WORK_MODE_ID=' || p_workmode_id);

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.SHOW_WORKMODE');
    END SHOW_WORKMODE;

    PROCEDURE SHOW_ZONE(p_zone_nr IN VARCHAR2) IS

        v_route_zone_id qwh_route_zones.route_zone_id%TYPE;

    BEGIN
        qcmp_trace.proc('TRP_TRANSPORT_FOR_USER.SHOW_ZONE');
        qcmp_trace.param('p_zone_nr'
                        ,p_zone_nr);

        SELECT route_zone_id
        INTO   v_route_zone_id
        FROM   qwh_route_zones
        WHERE  qwh_route_zones.route_zone_nr = p_zone_nr;

        qsyp_actions.addaction('Q_ACTION_OPEN_FORM');
        qsyp_actions.addparam('FORMNAME'
                             ,'QWH_ROUTE_ZONES_FD');
        qsyp_actions.addparam('WORKMODE'
                             ,'EDIT');
        qsyp_actions.addparam('WHERE'
                             ,'ROUTE_ZONE_ID=' || v_route_zone_id);

        qcmp_trace.RETURN('TRP_TRANSPORT_FOR_USER.SHOW_ZONE');
    END SHOW_ZONE;

    /******************************************************************************/
    /* Name : ShowActiveRadioTerminals
    /* Author   : Pawe³ Stêpniowski
    /* Date : 2016.08.05
    /*----------------------------------------------------------------------------*/
    /* Purpose : Wyœwietla spreada Stany terminali w trybie szukaj¹cym
    /*           Umozliwi wybranie aktywnego terminala.
    /*----------------------------------------------------------------------------*/
    /* Parameter (I) :
    /*----------------------------------------------------------------------------*/
    /* Parameter (O) :
    /*----------------------------------------------------------------------------*/
    /* Exceptions :
    /******************************************************************************/
    PROCEDURE ShowActiveRadioTerminals AS
    BEGIN

        qsyp_actions.addaction('Q_ACTION_OPEN_FORM');
        qsyp_actions.addparam('FORMNAME'
                             ,'QWH_TR_TERMINAL_STATES');
        qsyp_actions.addparam('LOV_QUERY'
                             ,'(SELECT * FROM QWHV_RDT_TR_TERMINAL_STATES WHERE IS_LOGED_IN = ''T'')');
        qsyp_actions.addparam('SEARCHMODE'
                             ,'T');

    END ShowActiveRadioTerminals;

END TRP_TRANSPORT_FOR_USER;
