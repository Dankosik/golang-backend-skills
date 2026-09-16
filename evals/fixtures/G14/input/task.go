package fixture

import "database/sql"

func Convert(value sql.NullInt64) *int64 {
	return &value.Int64
}
