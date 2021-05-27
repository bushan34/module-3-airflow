<p>
<strong>Папка great_expectations</strong> - весь проект<br>
<strong>Файл data_docs.zip</strong> - архив со сгенерированной документацией<br>
<br>
  Проверена таблица слоя ODS: <strong>pro_ods_payment</strong><br>
В таблице проведена проверка на пустые значения(Null), кол-во строк, кол-во и имя столбцов.<br>
<br>
  expect_table_row_count_to_be_between(max_value=1100, min_value=900) - проверка на кол-во строк<br>
  expect_table_column_count_to_equal(value=8) - проверка кол-ва столбцов<br>
  expect_table_columns_to_match_ordered_list(column_list=['user_id', 'pay_doc_type', 'pay_doc_num', 'account', 'phone', 'billing_period', 'pay_date', 'sum']) - проверка имя столбцов<br>
  expect_column_values_to_not_be_null(column='user_id') - не содержит NULL, <br>
  так и в остальных столбцах: 'pay_doc_type', 'pay_doc_num', 'account', 'phone', 'billing_period', 'pay_date', 'sum'<br>
  expect_column_values_to_match_regex(column='account', regex='^FL-\d+$') - проверка аккаунта<br>
  expect_column_value_lengths_to_be_between(column='phone', min_value=10, max_value=12) - проверка длины номера телефона<br>
  expect_column_values_to_be_between(column='sum', max_value=None, min_value=1e-07, strict_max=False, strict_min=False) - сумма больше нуля.<br>
  <br>
  

