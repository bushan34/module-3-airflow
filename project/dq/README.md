<p>
--Папка great_expectations - весь проект<br>
--Файл data_docs.zip - архив со сгенерированной документацией<br>
<br>
  Проверены таблицы слоя ODS: <strong>ods_billing, ods_issue, ods_payment, ods_traffic.</strong><br>
По всем таблицам проведена проверка на пустые значения(Null), кол-во строк, кол-во и имя столбцов.<br>
Дополнительно проведены проверки в таблице:<br>
  <strong>ods_billing</strong><br>
  expect_column_values_to_match_regex(column='billing_period', regex='^\d{4}-\d{2}')-проверка даты "ГГГГ-ММ"<br>
  expect_column_distinct_values_to_equal_set(column='tariff', value_set=['Gigabyte', 'Maxi', 'Megabyte', 'Mini'])-проверка тарифов<br>
  <br>
  <strong>ods_issue</strong><br>
  expect_column_distinct_values_to_equal_set(column='service', value_set=['Connect', 'Disconnect', 'Setup Environment'])-проверка служб<br>
  <br>
  <strong>ods_payment</strong><br>
  expect_column_values_to_match_regex(column='account', regex='^FL-\d+$')-проверка аккаунта<br>
  expect_column_value_lengths_to_be_between(column='phone', min_value=10, max_value=12)-проверка длины номера телефона<br>
  <br>
  <strong>ods_traffic</strong><br>
  expect_column_values_to_match_regex(column='device_ip_addr', regex="^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$")-проверка IP адреса xxx.xxx.xxx.xxx<br>
</p>
