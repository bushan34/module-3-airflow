---STG
CREATE EXTERNAL TABLE nnaranov.pro_stg_payment
    (
        user_id bigint,
        pay_doc_type text,
        pay_doc_num bigint,
        account text,
        phone text,
        billing_period text,
        pay_date text,
        sum float
    )
location ('pxf://rt-2021-03-25-16-47-29-sfunu-final-project/payment/*/?PROFILE=gs:parquet')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');

---ODS
CREATE TABLE nnaranov.pro_ods_payment
    (
        user_id int,
        pay_doc_type varchar,
        pay_doc_num int,
        account varchar,
        phone varchar,
        billing_period varchar,
        pay_date DATE,
        sum DEC(8,2)
    );
INSERT INTO nnaranov.pro_ods_payment
SELECT user_id, pay_doc_type, pay_doc_num, account, phone, billing_period, cast(pay_date as DATE), cast(sum as DECIMAL(8,2))
FROM nnaranov.pro_stg_payment;
---
CREATE TABLE nnaranov.pro_ods_mdm
    (
        id int,
        legal_type text,
        district text,
        registered_at timestamp,
        billing_mode text,
        is_vip boolean
    );
INSERT INTO nnaranov.pro_ods_mdm
SELECT * FROM mdm.user;

-------DDS
---DDS-HUB
CREATE TABLE nnaranov.pro_dds_hub_account
    (
        account_pk text,
        account_key varchar,
        load_date timestamp,
        record_source varchar
    )
DISTRIBUTED RANDOMLY;
---
CREATE TABLE nnaranov.pro_dds_hub_billing_period
(
	billing_period_pk text,
	billing_period_key varchar,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;
---
CREATE TABLE nnaranov.pro_dds_hub_pay_doc
(
	pay_doc_pk text,
	pay_doc_type_key varchar,
	pay_doc_num_key varchar,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;
---
CREATE TABLE nnaranov.pro_dds_hub_user
(
	user_pk text,
	user_key varchar,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;

---DDS-LINK
CREATE TABLE nnaranov.pro_dds_link_user_account_billing_pay
(
	user_account_billing_pay_pk text,
	user_pk text,
	account_pk text,
	billing_period_pk text,
	pay_doc_pk text,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;

---DDS-SAT
CREATE TABLE nnaranov.pro_dds_sat_user_details
(
	user_pk text,
	user_hashdiff text,
	phone varchar,
	effective_from date,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;
---
CREATE TABLE nnaranov.pro_dds_sat_pay_details
(
	user_account_billing_pay_pk text,
	pay_doc_hashdiff text,
	pay_date date,
	sum dec(8,2),
	effective_from date,
	load_date timestamp,
	record_source varchar
)
DISTRIBUTED RANDOMLY;

---Report_MDM
CREATE TABLE nnaranov.pro_payment_report_dim_billing_year (id SERIAL PRIMARY KEY, billing_year_key INT);
CREATE TABLE nnaranov.pro_payment_report_dim_legal_type (id SERIAL PRIMARY KEY, legal_type_key TEXT);
CREATE TABLE nnaranov.pro_payment_report_dim_district (id SERIAL PRIMARY KEY, district_key TEXT);
CREATE TABLE nnaranov.pro_payment_report_dim_registration_year (id SERIAL PRIMARY KEY, registration_year_key INT);
CREATE TABLE nnaranov.pro_payment_report_fact (
    billing_year_id INT,
    legal_type_id INT,
    district_id INT,
    registration_year_id INT,
    billing_mode TEXT,
    is_vip BOOLEAN,
    sum NUMERIC,
    CONSTRAINT fk_billing_year FOREIGN KEY (billing_year_id) REFERENCES nnaranov.pro_payment_report_dim_billing_year(id),
	CONSTRAINT fk_district FOREIGN KEY (district_id) REFERENCES nnaranov.pro_payment_report_dim_district(id),
	CONSTRAINT fk_legal_type FOREIGN KEY (legal_type_id) REFERENCES nnaranov.pro_payment_report_dim_legal_type(id),
	CONSTRAINT fk_registration_year FOREIGN KEY (registration_year_id) REFERENCES nnaranov.pro_payment_report_dim_registration_year(id)
);
---