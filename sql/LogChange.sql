CREATE OR ALTER PROCEDURE LogChange
    @��������������� INT,
    @���������� NVARCHAR(32),
    @����������� NVARCHAR(16),
    @������������� NVARCHAR(32),
    @������ NVARCHAR(32),
    @��������� NVARCHAR(32)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO ��������������� (
        ���������������,
        �������������,
        ����������,
        �����������,
        �������������,
        ������,
        ���������
    )
    VALUES (
        @���������������,
        GETDATE(),
        @����������,
        @�����������,
        @�������������,
        @������,
        @���������
    )
END