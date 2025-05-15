CREATE OR ALTER PROCEDURE ProcUpdateField
    @ID INT,
    @ИмяПоля NVARCHAR(128),
    @НовоеЗначение NVARCHAR(512)
AS
BEGIN
    SET NOCOUNT ON;

    -- Проверка на существование поля
    IF NOT EXISTS (
        SELECT 1
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Реагенты' AND COLUMN_NAME = @ИмяПоля
    )
    BEGIN
        RAISERROR('Поле %s не существует в таблице Реагенты.', 16, 1, @ИмяПоля)
        RETURN
    END

    -- Делаем запрос и выполняем его
    DECLARE @Sql NVARCHAR(MAX)
    SET @Sql = '
        UPDATE Реагенты
        SET [' + @ИмяПоля + '] = @НовоеЗначение
        WHERE КодРеагента = @ID
    '

    EXEC sp_executesql @Sql,
        N'@ID INT, @НовоеЗначение NVARCHAR(512)',
        @ID = @ID, @НовоеЗначение = @НовоеЗначение
END