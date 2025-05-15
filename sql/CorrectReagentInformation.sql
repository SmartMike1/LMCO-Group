CREATE OR ALTER PROCEDURE CorrectReagentInformation
	-- Add the parameters for the stored procedure here
	@Param1 int
AS
BEGIN
	SELECT * FROM Реагенты 
	WHERE КодРеагента = @Param1
END