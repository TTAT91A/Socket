CREATE DATABASE Temp_socket
GO
USE Temp_socket
GO
CREATE TABLE _VALUE(
	buy VARCHAR(10),
	sell VARCHAR(20),
	company VARCHAR(10), 
	brand NVARCHAR(20), 
	updated DATETIME, 
	brand1 NVARCHAR(20), 
	day DATE, 
	id VARCHAR(20), 
	type VARCHAR(50), 
	code VARCHAR(10)
)
SELECT BulkColumn
 INTO #temp 
 FROM OPENROWSET (BULK 'D:\HCMUS\21-22\MMT\Socket\Gold1207.json', SINGLE_CLOB) as j