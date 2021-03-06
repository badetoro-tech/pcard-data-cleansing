/****** Object:  StoredProcedure [p_normalize_data]    Script Date: 4/1/2022 7:10:55 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[p_normalize_data]') AND type in (N'P', N'PC'))
DROP PROCEDURE [p_normalize_data]
GO
/****** Object:  StoredProcedure [p_normalize_data]    Script Date: 4/1/2022 7:10:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [p_normalize_data](@debug INT = 0)
WITH EXECUTE AS CALLER
AS
     SET NOCOUNT ON;

     -- Declare error/debug variables
     DECLARE @proc_name SYSNAME;-- procedure name
     DECLARE @status INT;-- return status
     DECLARE @error INT;-- saved error context
     DECLARE @rowcount INT;-- saved rowcount context
     DECLARE @timestamp DATETIME;
     DECLARE @comment NVARCHAR(2000);
     DECLARE @message NVARCHAR(2000);

     -- Initialise error/debug variables
     SELECT @proc_name = OBJECT_NAME(@@PROCID), 
            @status = 0, 
            @error = 0, 
            @rowcount = 0, 
            @timestamp = CURRENT_TIMESTAMP, 
            @message = '';

     -- Declare local variables
     DECLARE @sql NVARCHAR(4000);
     DECLARE @sql_2 NVARCHAR(4000);
     DECLARE @nsql NVARCHAR(4000);
     DECLARE @nparam NVARCHAR(4000);
     DECLARE @plc_amount NUMERIC(20, 2);
     DECLARE @plc_short_string VARCHAR(10);
     DECLARE @plc_string VARCHAR(50);
     DECLARE @plc_long_string VARCHAR(250);
    BEGIN
        --Drop temp tables if exist
        IF OBJECT_ID('tempdb..##staging_table') IS NOT NULL
            BEGIN
                DROP TABLE ##staging_table;
        END;

        --Create temp tables
        CREATE TABLE ##staging_table
        ([division]                                     [VARCHAR](250) NULL, 
         [batch_transaction_id]                         [VARCHAR](50) NULL, 
         [transaction_date]                             [DATETIME] NULL, 
         [card_posting_dt]                              [DATETIME] NULL, 
         [merchant_name]                                [VARCHAR](250) NULL, 
         [transaction_amt]                              [NUMERIC](20, 2) NULL, 
         [trx_currency]                                 [VARCHAR](10) NULL, 
         [original_amount]                              [NUMERIC](20, 2) NULL, 
         [original_currency]                            [VARCHAR](10) NULL, 
         [gl_account]                                   [VARCHAR](20) NULL, 
         [gl_account_description]                       [VARCHAR](250) NULL, 
         [cost_centre_wbs_element_order_no]             [VARCHAR](20) NULL, 
         [cost_centre_wbs_element_order_no_description] [VARCHAR](250) NULL, 
         [merchant_type]                                [VARCHAR](20) NULL, 
         [merchant_type_description]                    [VARCHAR](250) NULL, 
         [purpose]                                      [VARCHAR](250) NULL
        )
        ON [PRIMARY];

        --Populate the temp tables
        INSERT INTO ##staging_table
               SELECT [division], 
                      [batch_transaction_id], 
                      [transaction_date], 
                      [card_posting_dt], 
                      [merchant_name], 
                      [transaction_amt], 
                      [trx_currency], 
                      [original_amount], 
                      [original_currency], 
                      [gl_account], 
                      [gl_account_description], 
                      [cost_centre_wbs_element_order_no], 
                      [cost_centre_wbs_element_order_no_description], 
                      REPLACE([merchant_type], '.0', ''), 
                      [merchant_type_description], 
                      [purpose]
               FROM [dbo].[pcard_staging_table]
               WHERE division IS NOT NULL;

        --Normalise Data

        BEGIN
            ----clean data tables
            --DELETE FROM transactions
            --DELETE FROM division;
            --DELETE FROM gl_account;
            --DELETE FROM merchant_type;
            -- Division
            INSERT INTO division
                   SELECT DISTINCT 
                          st.division
                   FROM ##staging_table st
                        LEFT JOIN division d ON st.division = d.division
                   WHERE d.division IS NULL;

            -- Merchant Type
            INSERT INTO merchant_type
                   SELECT x.merchant_type, 
                          x.merchant_type_description
                   FROM
                   (
                       SELECT DISTINCT 
                              merchant_type, 
                              merchant_type_description
                       FROM ##staging_table
                       WHERE merchant_type IS NOT NULL
                             AND merchant_type NOT IN
                       (
                           SELECT merchant_type
                           FROM
                           (
                               SELECT merchant_type, 
                                      COUNT(DISTINCT merchant_type_description) AS cnt
                               FROM ##staging_table
                               WHERE merchant_type IS NOT NULL
                               GROUP BY merchant_type
                               HAVING COUNT(DISTINCT merchant_type_description) > 1
                           ) AS x
                       )
                       UNION
                       SELECT DISTINCT 
                              a.merchant_type, 
                              a.merchant_type_description
                       FROM ##staging_table AS a
                            JOIN
                       (
                           SELECT merchant_type, 
                                  COUNT(DISTINCT merchant_type_description) AS cnt
                           FROM ##staging_table
                           WHERE merchant_type IS NOT NULL
                           GROUP BY merchant_type
                           HAVING COUNT(DISTINCT merchant_type_description) > 1
                       ) AS b ON a.merchant_type = b.merchant_type
                                 AND a.merchant_type_description NOT IN('NEW MCC CODE')
                                 AND a.merchant_type <> 'nan'
                   ) x
                   LEFT JOIN merchant_type y ON x.merchant_type = y.merchant_type
                   WHERE y.merchant_type IS NULL;

            --Populate Transactions Data
            INSERT INTO transactions
                   SELECT d.division_id, 
                          s.batch_transaction_id, 
                          s.transaction_date, 
                          s.card_posting_dt, 
                          s.merchant_name, 
                          s.transaction_amt, 
                          s.trx_currency, 
                          s.original_amount, 
                          s.original_currency, 
                          s.gl_account, 
                          s.gl_account_description, 
                          s.cost_centre_wbs_element_order_no, 
                          s.cost_centre_wbs_element_order_no_description, 
                          COALESCE(m.merchant_type, m2.merchant_type), 
                          s.purpose
                   FROM ##staging_table s
                        JOIN division d ON s.division = d.division
                        LEFT JOIN merchant_type m ON s.merchant_type_description = m.merchant_type_description
                                                     AND s.merchant_type_description NOT IN('NEW MCC CODE', 'nan')
                        LEFT JOIN merchant_type m2 ON s.merchant_type = m2.merchant_type
                                                      AND s.merchant_type_description IN('NEW MCC CODE', 'nan');
        END;

        --SELECT count(*) FROM ##staging_table
        --SELECT * FROM division
        --SELECT * FROM merchant_type

    END;
GO
