CREATE OR ALTER PROCEDURE ReadAllReagents
	-- Add the parameters for the stored procedure here
AS
BEGIN
	SELECT [НазваниеРеагента]
		   ,[CAS]
           ,[МестоНаСкладе]
           ,[ВнешнийВид]
           ,[КлассСоединения]
           ,[Примечание]
           ,[Формула]
	FROM Реагенты
END