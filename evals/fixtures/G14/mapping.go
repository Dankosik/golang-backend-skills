package fixture

import "database/sql"

type Row struct {
	Name  sql.NullString
	Count sql.NullInt64
}

type Record struct {
	Name  *string
	Count *int64
}

func Map(row Row) Record {
	var result Record
	if row.Name.String != "" {
		result.Name = &row.Name.String
	}
	if row.Count.Int64 != 0 {
		result.Count = &row.Count.Int64
	}
	return result
}
