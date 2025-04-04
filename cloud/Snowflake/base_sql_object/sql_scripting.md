# Snowflake scripting
- Mainly used in stored proc
- Variables
- if/else, case
- loops: for, repeat, while, loop
- cursors
- resultsets

Block structure : 
```sql
DECLARE
    -- Variables & cursor (optional)
BEGIN [NAME <name>]
    -- Scripting & SQL statements
    COMMIT
EXCEPTION
    -- errors handling (optional)
    ROLLBACK
END
```

Usage notes
- BEGIN is a synonym for `START TRANSACTION`
- To complete a transaction, a COMMIT or ROLLBACK command must be explicitly executed.
- When a transaction queries a stream, the timestamp used to get data when the transaction began the stream is queried at the stream advance point (i.e. the timestamp) rather than when the statement was run. This behavior pertains both to DML statements and CREATE TABLE … AS SELECT (CTAS) statements that populate a new table with rows from an existing stream.
- Objects created in a block can be used outside the block.
- Variables created in a block can only be used inside the block
