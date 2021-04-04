use covid;

bulk insert dbo.husa
  from 'C:\Users\ccc31\covid-data\psam_husa.csv'
  with (
    datafiletype = 'char',
	fieldterminator = ',',
	rowterminator = '0x0a',
	firstrow = 2,
	format = 'csv'
	);
bulk insert dbo.husa
  from 'C:\Users\ccc31\covid-data\psam_husb.csv'
  with (
    datafiletype = 'char',
	fieldterminator = ',',
	rowterminator = '0x0a',
	firstrow = 2,
	format = 'csv'
	);
--(788908 rows affected)

--(759280 rows affected)

--(1658808 rows affected)

--(1580745 rows affected)


bulk insert dbo.pusa
  from 'C:\Users\ccc31\covid-data\psam_pusa.csv'
  with (
    datafiletype = 'char',
	fieldterminator = ',',
	rowterminator = '0x0a',
	firstrow = 2,
	format = 'csv'
	);
bulk insert dbo.pusa
  from 'C:\Users\ccc31\covid-data\psam_pusb.csv'
  with (
    datafiletype = 'char',
	fieldterminator = ',',
	rowterminator = '0x0a',
	firstrow = 2,
	format = 'csv'
	);

