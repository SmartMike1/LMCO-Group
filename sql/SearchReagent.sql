CREATE OR ALTER PROCEDURE SearchReagent 
	-- Add the parameters for the stored procedure here
	@Param1 nvarchar(100)
AS
BEGIN
	SELECT * FROM Реагенты 
	WHERE CAS = @Param1 OR НазваниеРеагента LIKE @Param1 + N'%'
END