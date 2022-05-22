CREATE DATABASE TH_Socket
GO

USE TH_Socket
GO
CREATE TABLE DATA(
	type VARCHAR(10),
	imageurl VARCHAR(max),
	muatienmat VARCHAR(20),
	muack VARCHAR(20),
	bantienmat VARCHAR(20),
	banck VARCHAR(20),
	thoigian VARCHAR(20),
	updated VARCHAR(50)
)
delete from DATA;