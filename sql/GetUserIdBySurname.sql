CREATE OR ALTER PROCEDURE GetUserIdBySurname
    @������� NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP 1 ���������������
    FROM ������������
    WHERE ��� = @�������
END