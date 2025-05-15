CREATE OR ALTER PROCEDURE ProcUpdateField
    @ID INT,
    @������� NVARCHAR(128),
    @������������� NVARCHAR(512)
AS
BEGIN
    SET NOCOUNT ON;

    -- �������� �� ������������� ����
    IF NOT EXISTS (
        SELECT 1
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '��������' AND COLUMN_NAME = @�������
    )
    BEGIN
        RAISERROR('���� %s �� ���������� � ������� ��������.', 16, 1, @�������)
        RETURN
    END

    -- ������ ������ � ��������� ���
    DECLARE @Sql NVARCHAR(MAX)
    SET @Sql = '
        UPDATE ��������
        SET [' + @������� + '] = @�������������
        WHERE ����������� = @ID
    '

    EXEC sp_executesql @Sql,
        N'@ID INT, @������������� NVARCHAR(512)',
        @ID = @ID, @������������� = @�������������
END